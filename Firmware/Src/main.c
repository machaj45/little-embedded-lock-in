/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2020 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* USER CODE END Header */

/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "dac.h"
#include "dma.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#define LINESIZE 100
#define rx_buffer_size 100
#define BUF 32
#include "tables.h"
#include <stdarg.h>
#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include <string.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint32_t genFreq [2];
uint32_t sweepFreq [4];
uint16_t genBuffer1[4096];
uint16_t genBuffer2[4096];
uint16_t bufferSize1=BUF; // 1256
uint16_t bufferSize2=16;
uint8_t Rx_data ;
char Rx_Buffer [rx_buffer_size];
uint8_t Rx_indx = 0;
uint16_t prescaler0[2];
uint16_t autoReloadReg0[2];
uint16_t prescaler1[2];
uint16_t autoReloadReg1[2];
uint16_t autoReloadReg=10000;
uint16_t autoReloadRegX=10000;
uint16_t prescaler=0;

uint16_t fstep0=1;
uint16_t fstep1=1;
uint16_t sweepPathPos0=0;
uint16_t sweepPathPos1=0;
uint16_t sweepPathPos0stop=1;
uint16_t sweepPathPos1stop=1;
uint16_t offset0=0;
uint16_t offset1=0;
uint32_t realFreq1,realFreq2,realSampling;
uint32_t frek ;
uint32_t posun ;
double ref1;
double dut;
double ref2;
int32_t mref1=0;
int32_t mdut=0;
double gmref1=1.6;
double gmdut=1.6;
double mref2;
double X;
double Y;
double scale0=1.0;
double scale1=1.0;
volatile  uint8_t Transfer_cplt =0;
volatile uint8_t start = 0;
volatile uint8_t measuring = 0;
volatile uint8_t stop = 0;
volatile uint8_t step = 0;
volatile uint8_t freq = 0;
volatile uint8_t freqstart = 0;
volatile uint8_t freqstop = 0;
volatile uint8_t channel = 0;
volatile double xf=0;
volatile double yf=0;
volatile uint8_t upDown = 0;
volatile uint8_t sweep = 0;
volatile uint8_t togglesweep = 0;
volatile uint8_t sweep0 = 0;
volatile uint8_t sweep1 = 0;
volatile uint8_t posintable0 =0;
volatile uint8_t posintable1 =0;
volatile uint8_t positino0 =0;
volatile uint8_t positino1 =0;
volatile uint8_t ampl=0;
volatile uint8_t off=0;
volatile uint8_t adcintcounter=1;
volatile uint8_t adcintcountercheck=0;
volatile uint8_t adcenabled=1;
volatile uint8_t sin_square=1;

volatile uint8_t dataready = 0;
volatile uint8_t setfilter = 0;
volatile uint8_t printData = 0;
volatile uint8_t measure = 0;
volatile uint8_t samplerate = 0;
volatile uint8_t complete = 0;
volatile uint8_t half= 0;
volatile uint8_t transmitdone=0;
volatile uint8_t samplecounter=0;
volatile uint8_t firstsample = 0;
int samples = 4096;
int adcsamples=8;
int command = 0;
uint32_t data[10000];
float send [2];
double A = 0.001;

typedef struct PSARRFREQ {
	uint16_t prescaler;
	uint16_t autoReloadReg;
	uint32_t freq;
} PSARRFREQ;

PSARRFREQ pafa0 [LINESIZE];
PSARRFREQ pafa1 [LINESIZE];

uint8_t timReconfigure(TIM_HandleTypeDef* htim_base, uint32_t periphClock,
		uint32_t samplingFreq, uint32_t* realFreq, uint8_t isFreqPassed) {

	int32_t clkDiv;
	uint32_t errMinRatio = 0;
	uint8_t result = 1;
	uint16_t prescaler=0;
	uint16_t autoReloadReg;



	if (isFreqPassed == 1) {
		clkDiv = ((2 * periphClock / samplingFreq) + 1) / 2; //to minimize rounding error
	} else {
		clkDiv = samplingFreq;
	}

	if (clkDiv == 0) { //error
		result = 1;
	} else if (clkDiv <= 0x0FFFF) { //Sampling frequency is high enough so no prescaler needed
		prescaler = 0;
		autoReloadReg = clkDiv - 1;
		result = 0;
	} else {	// finding prescaler and autoReload value
		uint32_t errVal = 0xFFFFFFFF;
		uint32_t errMin = 0xFFFFFFFF;
		uint16_t ratio = clkDiv >> 16;
		uint16_t div;

		while (errVal != 0) {
			ratio++;
			div = clkDiv / ratio;
			errVal = clkDiv - (div * ratio);

			if (errVal < errMin) {
				errMin = errVal;
				errMinRatio = ratio;
			}

			if (ratio == 0xFFFF) { //exact combination wasnt found. we use best found
				div = clkDiv / errMinRatio;
				ratio = errMinRatio;
				break;
			}
		}

		//if (ratio > div) {
			prescaler = div - 1;
			autoReloadReg = ratio - 1;
		//} else {
		//	prescaler = ratio - 1;
		//	autoReloadReg = div - 1;
		//}

		if (errVal) {
			result = 1;
		} else {
			result = 0;
		}
	}

	if (realFreq != 0) {
		*realFreq = periphClock / ((prescaler + 1) * (autoReloadReg + 1));
	}

	htim_base->Instance->PSC = prescaler;
	htim_base->Instance->ARR = autoReloadReg;

	SET_BIT(htim_base->Instance->EGR, TIM_EGR_UG);
	return (result);
}
uint8_t timReconfigureForGenerator(uint32_t samplingFreq,uint8_t chan,uint32_t* realFreq){
	/* RCC_PERIPHCLK_TIM6 and TIM7 defines missing in order to use with HAL_RCCEx_GetPeriphCLKFreq fun */
	uint32_t periphClock = HAL_RCC_GetPCLK1Freq()*2;
	if(chan==0){
		return (timReconfigure(&htim6,periphClock,samplingFreq,realFreq,1));
	}else if(chan==1){
		return (timReconfigure(&htim7,periphClock,samplingFreq,realFreq,1));
	}else{
		return (0);
	}
}
PSARRFREQ setFreq(uint32_t samplingFreq) {
	int32_t clkDiv;
	uint32_t errMinRatio = 0;

	uint16_t prescaler=0;
	uint16_t autoReloadReg;
	PSARRFREQ pafa;
	uint32_t periphClock = HAL_RCC_GetPCLK1Freq()*2;
	clkDiv = ((2 * periphClock / samplingFreq) + 1) / 2; //to minimize rounding error
	if (clkDiv == 0) { //error

	} else if (clkDiv <= 0x0FFFF) { //Sampling frequency is high enough so no prescaler needed
		prescaler = 0;
		autoReloadReg = clkDiv - 1;

		pafa.autoReloadReg = autoReloadReg;
		pafa.prescaler =prescaler;
		pafa.freq =samplingFreq;
	} else {	// finding prescaler and autoReload value
		uint32_t errVal = 0xFFFFFFFF;
		uint32_t errMin = 0xFFFFFFFF;
		uint16_t ratio = clkDiv >> 16;
		uint16_t div;

		while (errVal != 0) {
			ratio++;
			div = clkDiv / ratio;
			errVal = clkDiv - (div * ratio);

			if (errVal < errMin) {
			errMin = errVal;
			errMinRatio = ratio;
			}

			if (ratio == 0xFFFF) { //exact combination wasnt found. we use best found
			div = clkDiv / errMinRatio;
			ratio = errMinRatio;
			break;
			}
		}

	//	if (ratio > div) {
			prescaler = div - 1;
			autoReloadReg = ratio - 1;
	//	} else {
	//		prescaler = ratio - 1;
	//		autoReloadReg = div - 1;
	//	}
		pafa.autoReloadReg = autoReloadReg;
		pafa.prescaler =prescaler;
		pafa.freq =samplingFreq;
	}
	return (pafa);
}
int setPath(uint32_t minF,uint32_t maxF,uint16_t step,uint16_t size,int channel){
	if(channel==0){
		if(step==0 && size!=0){
			uint32_t freq;
			uint16_t index = 0;
			freq = minF;
			step = (uint16_t)((maxF*1.0-minF*1.0)/(size*1.0));
			while(index<=size&& index<=LINESIZE){
				pafa0[index] = setFreq(freq);
				freq+=step;
				index++;
			}
			return (--index);
		}else if (step!=0 && size==0){
			uint32_t freq;
			uint16_t index = 0;
			freq = minF;
			PSARRFREQ temp;
			while(freq < maxF-step && index<=LINESIZE){
				temp = setFreq(freq);
				pafa0[index].autoReloadReg = temp.autoReloadReg;
				pafa0[index].prescaler = temp.prescaler;
				pafa0[index].freq = temp.freq;
				freq+=step;
				index++;
			}
			return (--index);
		}else{
			return (-1);
		}
	}
	if(channel==1){
		if(step==0 && size!=0){
			uint32_t freq;
			uint16_t index = 0;
			freq = minF;
			step = (uint16_t)((maxF*1.0-minF*1.0)/(size*1.0));
			while(index<=size&& index<=LINESIZE){
				pafa1[index] = setFreq(freq);
				freq+=step;
				index++;
			}
			return (--index);
		}else if (step!=0 && size==0){
			uint32_t freq;
			uint16_t index = 0;
			freq = minF;
			while(freq < maxF-step && index<=LINESIZE){
				pafa1[index] = setFreq(freq);
				freq+=step;
				index++;
			}
			return (--index);
		}else{
			return (-1);
		}
	}
	return (-1);
}
void buffersInit(const  uint16_t * buf,uint16_t size,double scale,uint16_t offset){
	uint16_t temp;
	if(sin_square==1){
		if(channel==0){
			bufferSize1=size;
			for (int i = 0; i < bufferSize1; ++i) {
				temp=(uint16_t)(buf[i]*scale*1.0)+offset;
				if(temp>4095){
				 genBuffer1[i]=4095;
				}else{
					genBuffer1[i]=temp;
				}
			}
		}
		if(channel==1){
			bufferSize2=size;
			for (int i = 0; i < bufferSize2; ++i) {
				temp=(uint16_t)(buf[i]*scale*1.0)+offset;
				if(temp>4095){
					genBuffer2[i]=4095;
				}else{
					genBuffer2[i]=temp;
				}
			}

		}
	}
	if(sin_square==0){
		if(channel==0){
			bufferSize1=size;
			for (int i = 0; i < bufferSize1; ++i) {
				if(i<bufferSize1/2){
					temp=(uint16_t)offset;
				}else{
					temp=(uint16_t)(4095*scale*1.0)+offset;
				}
				if(temp>4095){
				 genBuffer1[i]=4095;
				}else{
					genBuffer1[i]=temp;
				}
			}
		}
		if(channel==1){
			bufferSize2=size;
			for (int i = 0; i < bufferSize2; ++i) {
				if(i<bufferSize1/2){
					temp=(uint16_t)offset;
				}else{
					temp=(uint16_t)(4095*scale*1.0)+offset;
				}
				if(temp>4095){
					genBuffer2[i]=4095;
				}else{
					genBuffer2[i]=temp;
				}
			}

		}

	}
}
void initBuffers(int size,double scale,uint16_t offset){
	if(scale==0){return ;}
	switch(size){
		case 16 :size = 16;buffersInit(sin_samples16,size,scale,offset);break;
		case 32 :size = 32;buffersInit(sin_samples32,size,scale,offset);break;
		case 64 :size = 64;buffersInit(sin_samples64,size,scale,offset);break;
		case 128 :size = 128;buffersInit(sin_samples128,size,scale,offset);break;
		case 256 :size = 256;buffersInit(sin_samples256,size,scale,offset);break;
		case 512 :size = 512;buffersInit(sin_samples512,size,scale,offset);break;
		case 1024 :size = 1024;buffersInit(sin_samples1024,size,scale,offset);break;
		case 2048 :size = 2048;buffersInit(sin_samples2048,size,scale,offset);break;
		case 4096 :size = 4096;buffersInit(sin_samples4096,size,scale,offset);break;
		default:size = 16;buffersInit(sin_samples16,size,scale,offset);break;
	}
}
int genInit(void)
{
		int status = 0;
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
		status=timReconfigureForGenerator(genFreq[0],0,&realFreq1);
		status=timReconfigureForGenerator(genFreq[1],1,&realFreq2);
		status=HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
		status=HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_2, (uint32_t*)genBuffer2,bufferSize2, DAC_ALIGN_12B_R);
		return (status);
}
int genInit0(void)
{
		int status = 0;
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);
		status=timReconfigureForGenerator(genFreq[0],0,&realFreq1);
		status=HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
		return (status);
}
int genInit1(void)
{
		int status = 0;
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
		status=timReconfigureForGenerator(genFreq[1],1,&realFreq2);
		status=HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_2, (uint32_t*)genBuffer2,bufferSize2, DAC_ALIGN_12B_R);
		return (status);
}
void DACDisableOutput0(void){
  GPIO_InitTypeDef GPIO_InitStruct;
  GPIO_InitStruct.Pin = G1_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
void DACDisableOutput1(void){
  GPIO_InitTypeDef GPIO_InitStruct;
  GPIO_InitStruct.Pin = G2_Pin;
  GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);
}
int genStop0(void)
{
		int status = 0;
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);
		DACDisableOutput0();
		return (status);
}
int genStop1(void)
{
		int status = 0;
		HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
		DACDisableOutput1();
		return (status);
}

void vprint(const char *fmt, va_list argp)
{
	char string[300];
    if(0 < vsprintf(string,fmt,argp)) // build string
    {
    	//HAL_Delay(10);
        HAL_UART_Transmit(&huart2, (uint8_t*)string, strlen(string),0xFFFFF); // send message via UART
    }
}
void pr(const char *text, ...) // custom print() function
{
	HAL_Delay(10);
    va_list argp;
    va_start(argp, text);
    vprint(text, argp);
    va_end(argp);
}
void setSweepMaxMin(int newinput){
	if(sweep==1 && command==0 && newinput > 0){
		sweep=0;
		sweepFreq[2*channel+upDown]=newinput*bufferSize1;
		pr("%d\n\r",newinput);
	}
}

void printADCOut(){
	//send[0]=(float)xf;
	//send[1]=(float)yf;
	//HAL_UART_Transmit(&huart2, (uint8_t*)(&send), 8,0xFFFFF);

	if(dataready==0){
		pr("DNR\n\r");
	}
	if(dataready==2){
		dataready = 0;
		HAL_Delay(10);
		HAL_UART_Transmit(&huart2, (uint8_t*)(&data), samples*4,0xFFFF);
	}
	if(dataready==1){
		pr("MD\n\r");
		dataready = 2;
	}


}
uint16_t selectBufferSize(uint32_t frequency){
	uint16_t option = 4096;
	for (uint i = 1255;i<=321280;i=i*2){
		option=option/2;
		if(frequency<i*2&&i<frequency){
			return (option/2);
		}

	}
	return (4096);
}
void setAmpl(int newinput){
	if(ampl==1 && command==0 && newinput > 0){
		ampl=0;
		if(channel==0){
			scale0 = (double)(newinput/100.0);
			if(scale0>=100.0){
				scale0=100.0;
			}
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);
			uint16_t temparr = htim6.Instance->ARR;
			uint16_t temppsc = htim6.Instance->PSC;
			htim6.Instance->ARR = 3999;
			htim6.Instance->PSC = 9;
			initBuffers(bufferSize1, scale0, offset0);
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
			htim6.Instance->ARR = temparr;
			htim6.Instance->PSC = temppsc;
			pr("%d\n\r",newinput);
		}
		if(channel==1){
			scale1 =  (double)(newinput/100.0);
			if(scale1>=100.0){
				scale1=100.0;
			}
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
			uint16_t temparr = htim7.Instance->ARR;
			uint16_t temppsc = htim7.Instance->PSC;
			htim7.Instance->ARR = 3999;
			htim7.Instance->PSC = 9;
			initBuffers(bufferSize2, scale1, offset1);
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_2, (uint32_t*)genBuffer2,bufferSize2, DAC_ALIGN_12B_R);
			htim7.Instance->ARR = temparr;
			htim7.Instance->PSC = temppsc;
			pr("%d\n\r",newinput);
		}
	}
}

void setFiltr(int newinput){
	if(setfilter==1 && command==0 && newinput > 0){
		setfilter=0;
		A = ((double)newinput)/100000.0;
		pr("%.6f\n\r",(float)A);
	}
}
void setFrequency(int newinput){
	if(freq==1 && command==0 && newinput > 0){
		freq=0;
		if(channel==0){
			sweep0=0;
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);

			htim6.Instance->ARR = 3999;
			htim6.Instance->PSC = 9;
			bufferSize1 = selectBufferSize(newinput);
			initBuffers(bufferSize1, scale0, offset0);
			genFreq[0]=newinput*bufferSize1;
			posintable0=0;
			posintable1=0;
			timReconfigureForGenerator(genFreq[0],0,&realFreq1);
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
			pr("%.3f\n",(float)realFreq1/(float)bufferSize1);
			//pr("%d\n\r",newinput);
			//setAmpl(scale0);
		}
		if(channel==1){
			sweep1=0;
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
			htim7.Instance->ARR = 3999;
			htim7.Instance->PSC = 9;
			bufferSize2 = selectBufferSize(newinput);
			initBuffers(bufferSize2, scale1, offset1);
			genFreq[1]=newinput*bufferSize2;
			posintable0=0;
			posintable1=0;
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_2, (uint32_t*)genBuffer2,bufferSize2, DAC_ALIGN_12B_R);
			timReconfigureForGenerator(genFreq[1],1,&realFreq2);
			//pr("%d\n\r",newinput);
			pr("%.3f\n",(float)realFreq2/(float)bufferSize2);
		}
	}
}
void setStep(int newinput){
	if(step==1 && command==0 && newinput > 0){
		step=0;
		if(channel==0){
			fstep0 = newinput*bufferSize1;
			pr("%d\n\r",newinput);
		}
		if(channel==1){
			fstep1 = newinput*bufferSize2;
			pr("%d\n\r",newinput);
		}
	}
}
void setSampleRate(int newinput){
	if(samplerate==1 && command==0 && newinput > 0){
		samplerate=0;
		adcsamples = newinput;
		pr("%d\n\r",adcsamples);
	}
}
void setOffset(int newinput){
	if(off==1 && command==0 && newinput > 0){
		off=0;
		if(newinput ==5000)
			newinput =0;
		if(channel==0){
			offset0 = newinput;
			uint32_t temparr = htim6.Instance->ARR;
			uint32_t temppsc = htim6.Instance->PSC;
			htim6.Instance->ARR = 3999;
			htim6.Instance->PSC = 9;
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_1);
			initBuffers(bufferSize1, scale0, offset0);
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
			htim6.Instance->ARR = temparr;
			htim6.Instance->PSC = temppsc;
			pr("%d\n\r",newinput);
		}
		if(channel==1){
			offset1 = newinput;
			HAL_DAC_Stop_DMA(&hdac1,DAC_CHANNEL_2);
			uint32_t temparr = htim7.Instance->ARR;
			uint32_t temppsc = htim7.Instance->PSC;
			htim7.Instance->ARR = 3999;
			htim7.Instance->PSC = 9;
			initBuffers(bufferSize2, scale1, offset1);
			HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_2, (uint32_t*)genBuffer2,bufferSize2, DAC_ALIGN_12B_R);
			htim7.Instance->ARR = temparr;
			htim7.Instance->PSC = temppsc;
			pr("%d\n\r",newinput);
		}
	}
}
void sweepUpdate(){
	if(sweep0==1){
		htim6.Instance->ARR = pafa0[sweepPathPos0].autoReloadReg;
		htim6.Instance->PSC = pafa0[sweepPathPos0].prescaler;
		if(sweepPathPos0stop>sweepPathPos0){
			sweepPathPos0++;
		}else{
			sweepPathPos0=0;
		}
	}
	if(sweep1==1){
		htim7.Instance->ARR = pafa1[sweepPathPos1].autoReloadReg;
		htim7.Instance->PSC = pafa1[sweepPathPos1].prescaler;
		if(sweepPathPos1stop>sweepPathPos1){
			sweepPathPos1++;
		}else{
			sweepPathPos1=0;
		}
	}
}

void toggleSweep(){
	if(togglesweep==1){
		togglesweep=0;
		if(channel==0){
			if(sweep0==0){

				sweepPathPos0=0;
				sweepPathPos0stop=setPath(sweepFreq[0], sweepFreq[1], fstep0, 0, 0);
				sweep0=1;
			}
			else if(sweep0==1)
				sweep0=0;
		}
		if(channel==1){
			if(sweep1==0){

				sweepPathPos1=0;
				sweepPathPos1stop=setPath(sweepFreq[2], sweepFreq[3], fstep1, 0, 1);
				sweep1=1;
			}
			else if(sweep1==1)
				sweep1=0;
		}
	}
}
int compare_strings(char a[], char b[])
{
   int c = 0;

   while (a[c] == b[c]) {
      if (a[c] == '\n' || b[c] == '\n')
         break;
      c++;
   }

   if (a[c] == '\n' && b[c] == '\n')
      return (0);
   else
      return (-1);
}
int getRequest(){
	char buf1 [5] = {'I','D','N','?','\n'};
	char buf2 [5] = {'V','E','R','?','\n'};
	char buf3 [5] = {'F','R','Q','?','\n'};
	char buf4 [5] = {'F','R','Q','!','\n'};
	char buf5 [6] = {'S','T','A','R', 'T','\n'};
	char buf6 [5] = {'S','T','O','P','\n'};
	char buf7 [2] = {'0','\n'};
	char buf8 [2] = {'1','\n'};
	char buf9 [5] = {'S','W','E','P','\n'};
	char buf10 [2] = {'D','\n'};
	char buf11 [2] = {'U','\n'};
	char buf12 [6] = {'S','W','E','P','S','\n'};
	char buf13 [5] = {'S','T','E','P','\n'};
	char buf14 [5] = {'A','M','P','L','\n'};
	char buf15 [5] = {'O','F','F','S','\n'};
	char buf16 [5] = {'D','A','T','A','\n'};
	char buf17 [5] = {'M','E','A','S','\n'};
	char buf18 [5] = {'S','A','M','P','\n'};
	char buf19 [5] = {'F','I','L','T','\n'};
	char buf20 [5] = {'S','I','N','S','\n'};

	if(compare_strings(buf1,Rx_Buffer)==0){
		command = 0;
		return (1);
	}
	if(compare_strings(buf2,Rx_Buffer)==0){
		command = 0;
		return (2);
	}
	if(compare_strings(buf3,Rx_Buffer)==0){
		command = 0;
		return (3);
	}
	if(compare_strings(buf4,Rx_Buffer)==0){
		command = 1;
		freq=1;
		return (4);
	}
	if(compare_strings(buf5,Rx_Buffer)==0){
		command = 1;
		start = 1;
		return (5);
	}
	if(compare_strings(buf6,Rx_Buffer)==0){
		command = 1;
		stop= 1;
		return (6);
	}
	if(compare_strings(buf7,Rx_Buffer)==0 && command==1){
		command = 0;
		channel=0;
		return (7);
	}
	if(compare_strings(buf8,Rx_Buffer)==0 && command==1){
		command = 0;
		channel=1;
		return (8);
	}
	if(compare_strings(buf9,Rx_Buffer)==0){
		command = 1;
		sweep = 1;
		return (9);
	}
	if(compare_strings(buf10,Rx_Buffer)==0 && sweep ==1){
		command = 0;
		upDown=0;
		return (7);
	}
	if(compare_strings(buf11,Rx_Buffer)==0  && sweep ==1){
		command = 0;
		upDown=1;
		return (8);
	}
	if(compare_strings(buf12,Rx_Buffer)==0 ){
		command = 1;
		if(togglesweep==0){
			togglesweep=1;
		}
		return (9);
	}
	if(compare_strings(buf13,Rx_Buffer)==0){
			command = 1;
			step = 1;
			return (10);
	}
	if(compare_strings(buf14,Rx_Buffer)==0){
			command = 1;
			ampl = 1;
			return (11);
	}
	if(compare_strings(buf15,Rx_Buffer)==0){
			command = 1;
			off = 1;
			return (12);
	}
	if(compare_strings(buf16,Rx_Buffer)==0){
			printData = 1;
			return (13);
	}
	if(compare_strings(buf17,Rx_Buffer)==0){
			measure = 1;
			return (14);
	}
	if(compare_strings(buf18,Rx_Buffer)==0){
			command = 0;
			samplerate = 1;
			return (15);
	}
	if(compare_strings(buf19,Rx_Buffer)==0){
			command = 0;
			setfilter = 1;
			return (15);
	}
	if(compare_strings(buf20,Rx_Buffer)==0){
			command = 0;
			if(sin_square==1)
			sin_square = 0;
			else
			sin_square = 1;
			return (16);
	}
	command = 0;
	return (0);
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) // @suppress("Name convention for function")
{
        if (huart->Instance == USART2){ // Current UART
		if (Rx_indx + 1 > rx_buffer_size){
			Rx_indx = 0;
		}
        if (Rx_data != 0x0A){ // If received data different from LF
        	Rx_Buffer[Rx_indx++] = Rx_data;    // Add data to Rx_Buffer
		}
		else {
			Rx_Buffer[Rx_indx++] = '\n';
			Rx_indx = 0;
			Transfer_cplt++;//transfer complete, data is ready to read
		}
		HAL_UART_Receive_IT(&huart2, &Rx_data, 1);   //activate UART receive interrupt every time
	}
}
void changeSamplingTime(uint32_t frek){
	uint32_t out = ADC_SAMPLETIME_1CYCLE_5 ;
	switch(frek){
		case 0       ... 117532: out = ADC_SAMPLETIME_601CYCLES_5;break;
		case 117533  ... 371984: out = ADC_SAMPLETIME_181CYCLES_5;break;
		case 371985  ... 975202: out = ADC_SAMPLETIME_61CYCLES_5;break;
		case 975203  ... 2255154:out = ADC_SAMPLETIME_19CYCLES_5;break;
		case 2255155 ... 3608247:out = ADC_SAMPLETIME_7CYCLES_5;break;
		case 3608248 ... 4244997:out = ADC_SAMPLETIME_4CYCLES_5;break;
		case 4244998 ... 4810996:out = ADC_SAMPLETIME_2CYCLES_5;break;
		case 4810997 ... 5154639:out = ADC_SAMPLETIME_1CYCLE_5;break;
		default:				 out = ADC_SAMPLETIME_1CYCLE_5;break;
	}
	ADC_ChannelConfTypeDef sConfig = {0};
	sConfig.Channel = ADC_CHANNEL_7;
	sConfig.Rank = ADC_REGULAR_RANK_1;
	sConfig.SingleDiff = ADC_SINGLE_ENDED;
	sConfig.SamplingTime = out;
	sConfig.OffsetNumber = ADC_OFFSET_NONE;
	sConfig.Offset = 0;
	if (HAL_ADC_ConfigChannel(&hadc2, &sConfig) != HAL_OK)
	{
		Error_Handler();
	}
	sConfig.Channel = ADC_CHANNEL_6;
	sConfig.Rank = ADC_REGULAR_RANK_1;
	sConfig.SingleDiff = ADC_SINGLE_ENDED;
	sConfig.SamplingTime = out;
	sConfig.OffsetNumber = ADC_OFFSET_NONE;
	sConfig.Offset = 0;
	if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
	{
		Error_Handler();
	}
}
void setADC(uint32_t samplesPerPeriod){
	frek = (uint32_t)(realFreq1*1.0/bufferSize1);
	//HAL_ADCEx_MultiModeStart_DMA(&hadc1,(uint32_t*)&data,samples);
	int status;
	//MX_ADC1_Init();
//	MX_ADC2_Init();
	posun = samplesPerPeriod>>2;
	uint32_t periphClock = HAL_RCCEx_GetPeriphCLKFreq(RCC_PERIPHCLK_TIM15);
	if(adcintcounter==0){
		status = HAL_ADCEx_MultiModeStop_DMA(&hadc1);
		status = HAL_ADC_Init(&hadc1);
		status = HAL_ADC_Stop_IT(&hadc2);
		HAL_TIM_Base_Start(&htim15);
	}

	status = timReconfigure(&htim15,periphClock,frek*samplesPerPeriod,&realSampling,1);
	changeSamplingTime(frek*samplesPerPeriod);
    HAL_TIM_Base_MspInit(&htim15);
	int a = 10000/samplesPerPeriod;
	samples=(a-1)*(samplesPerPeriod);
	status = HAL_ADC_Start(&hadc2);
	if (status == 2){
		HAL_ADC_Stop(&hadc2);
		status = HAL_ADC_Start(&hadc2);
	}

	//HAL_TIM_Base_Start_IT(&htim15);
	status = HAL_TIM_Base_Start(&htim15);
	complete=0;
	firstsample=0;
	SET_BIT(hadc1.Instance->CFGR, ADC_CFGR_DMAEN);
	status = HAL_ADCEx_MultiModeStart_DMA(&hadc1,(uint32_t*)&data,samples);
	if (status == 2){
		status = HAL_ADCEx_MultiModeStop_DMA(&hadc1);
		status = HAL_ADCEx_MultiModeStart_DMA(&hadc1,(uint32_t*)&data,samples);
	}
	adcintcounter = 0;
}

void  HAL_ADC_ConvHalfCpltCallback(ADC_HandleTypeDef* hadc){ // @suppress("Name convention for function")
	if(hadc != &hadc1)
			return;
}


void HAL_ADC_ConvCpltCallback(ADC_HandleTypeDef* hadc){ // @suppress("Name convention for function")
	if(hadc != &hadc1)
			return;
	//HAL_ADC_Stop(&hadc2);
	//
	complete=1;
	adcintcounter++;
	HAL_ADCEx_MultiModeStop_DMA(&hadc1);
	HAL_ADC_Init(&hadc1);
	HAL_ADC_Stop_IT(&hadc2);
	HAL_TIM_Base_Start(&htim15);
	dataready=1;
	//HAL_UART_Receive_IT(&huart2, &Rx_data, 1);

}

/* USER CODE END 0 */


int main(void)
{
  /* USER CODE BEGIN 1 */

	genFreq[0]=1000;
	genFreq[1]=1000;
  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_USART2_UART_Init();
  MX_DAC1_Init();
  MX_TIM6_Init();
  MX_TIM7_Init();
  MX_ADC1_Init();
  MX_ADC2_Init();
  MX_TIM15_Init();
  /* USER CODE BEGIN 2 */
  initBuffers(BUF,1,0);
  channel=1;
  initBuffers(16,0.7,150);
  channel=0;


	HAL_NVIC_SetPriority(USART2_IRQn, 0, 0);
	HAL_NVIC_EnableIRQ(USART2_IRQn);
	//HAL_NVIC_SetPriority(TIM6_DAC_IRQn, 2, 0);
	//HAL_NVIC_EnableIRQ(TIM6_DAC_IRQn);
	//HAL_NVIC_SetPriority(TIM7_IRQn, 0, 0);
	//HAL_NVIC_EnableIRQ(TIM7_IRQn);

	HAL_NVIC_SetPriority(TIM1_UP_TIM16_IRQn, 3, 0);
	HAL_NVIC_EnableIRQ(TIM1_UP_TIM16_IRQn);


	HAL_UART_Receive_IT(&huart2, &Rx_data, 1);

	//genInit();
	//HAL_TIM_Base_Start_IT(&htim6);
	HAL_TIM_Base_Start(&htim6);
	HAL_TIM_Base_MspInit(&htim6);
	//HAL_TIM_Base_Start_IT(&htim7);
	HAL_TIM_Base_Start(&htim7);
	HAL_TIM_Base_MspInit(&htim7);
	timReconfigureForGenerator(genFreq[0],0,&realFreq1);
	timReconfigureForGenerator(genFreq[1],1,&realFreq2);

	htim6.Instance->ARR = autoReloadReg;
	htim6.Instance->PSC = prescaler;
	SET_BIT(htim6.Instance->EGR, TIM_EGR_UG);
	htim7.Instance->ARR = autoReloadReg;
	htim7.Instance->PSC = prescaler;
	SET_BIT(htim7.Instance->EGR, TIM_EGR_UG);
	for (int i = 0 ;  i < 4096;i++){
		data[i]=0;
	}

	HAL_ADCEx_Calibration_Start(&hadc1,ADC_SINGLE_ENDED);
	HAL_ADCEx_Calibration_Start(&hadc2,ADC_SINGLE_ENDED);

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
	//uint16_t wgd = 0;
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */



	HAL_Delay(1);
	//wgd++;
	//if(wgd>1500){
	//	wgd=0;
	//	HAL_UART_Receive_IT(&huart2, &Rx_data, 1);
	//}
	if(complete==1){


//		status = HAL_ADCEx_InjectedStop(&hadc1);
//		status = HAL_ADC_Stop_DMA(&hadc1) ;
//		status = HAL_ADCEx_MultiModeStop_DMA(&hadc1);
//		status = HAL_ADC_Stop_DMA(&hadc2) ;
//		status = HAL_ADC_Stop(&hadc2);
//		status = HAL_ADC_Stop(&hadc1);

	//	HAL_DMA_DeInit(&hdma_adc1);
		//CLEAR_BIT(hadc2.Instance->CFGR, ADC_CFGR_DMAEN);
		//HAL_ADC_Init(&hadc1);
		//HAL_ADC_Init(&hadc2);
		complete=0;
	}
/*
	if(complete){
		transmitdone=0;
		complete=0;
		//HAL_ADCEx_MultiModeStop_DMA(&hadc1);
		//HAL_Delay(10);
		//HAL_ADCEx_MultiModeStop_DMA(&hadc1);
		HAL_UART_Transmit(&huart2, (uint8_t*)(&data), samples*4,0xFFFF);
		measuring=0;

			mref1=0;
			mdut=0;
			for (int i = 0;  i < samples; i++) {
				mref1 += ((uint16_t)data[i]&0x0000FFFF);
				mdut += ((uint16_t)(data[i]>>16)&0x0000FFFF);
			}
			mref1 = (int32_t) mref1/(double)(samples);
			mdut= (int32_t) mdut/(double)(samples);
			double a = 3.3/4096;
			for (int i = posun;  i < samples; i++) {
				ref1 = (((uint16_t)data[i]&0x0000FFFF))-mref1;
				dut = (((uint16_t)(data[i]>>16)&0x0000FFFF))-mdut;
				ref2 = (((uint16_t)data[i-posun]&0x0000FFFF))-mref1;
				ref1=ref1*a;
				dut=dut*a;
				ref2=ref2*a;
				X = ((double)(dut)*(double)(ref1));
				Y = ((double)(dut)*(double)(ref2));
				xf = A* X+(1-A)*xf;
				yf = A* Y+(1-A)*yf;
			}

		transmitdone=1;

		//HAL_ADCEx_MultiModeStart_DMA(&hadc1,(uint32_t*)&data,samples);


	}*/

	int newinput=0;
	if(Transfer_cplt!=0){
		switch(getRequest()){
			case 0:newinput= atoi(Rx_Buffer);break;
			case 1:pr("Lock-in Amplifier\n");sin_square=1;break;
			case 2:pr("Version 1.0.5\n");break;
			case 3:pr("Frequency is %d\n",100);break;
			case 4:;break;
			case 5:pr("Starting Generator\n");sweep0=0;break;
			case 6:pr("Stopping Generator\n");sweep1=0;break;

			default: break;
		}

		if(start==1 && channel==0){
				genInit0();
				start=0;
		}
		if(start==1 && channel==1){
			genInit1();
			start=0;
		}

		if(stop==1 && channel==0){
			genStop0();
			stop=0;
		}
		if(stop==1 && channel==1){
			genStop1();
			stop=0;
		}

		toggleSweep();
		setFrequency(newinput);
		setStep(newinput);
		setAmpl(newinput);
		setOffset(newinput);
		setSampleRate(newinput);
		setFiltr(newinput);


		if(measure==1){
			pr("MB\n\r");
			measure=0;
			xf=0;
			yf=0;
			dataready=0;
			adcintcountercheck=0;
			HAL_Delay(100);
			setADC(adcsamples);

		}
		setSweepMaxMin(newinput);
		newinput=0;
		//HAL_DAC_Start_DMA(&hdac1,DAC_CHANNEL_1, (uint32_t*)genBuffer1,bufferSize1, DAC_ALIGN_12B_R);
		if(printData==1 ){
			printData=0;
			//HAL_ADCEx_MultiModeStop_DMA(&hadc1);
			printADCOut();
		}
	}
	sweepUpdate();
	Transfer_cplt=0;
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void) // @suppress("Name convention for function")
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  RCC_OscInitStruct.PLL.PREDIV = RCC_PREDIV_DIV1;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB busses clocks 
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART2|RCC_PERIPHCLK_TIM15
                              |RCC_PERIPHCLK_ADC12;
  PeriphClkInit.Usart2ClockSelection = RCC_USART2CLKSOURCE_PCLK1;
  PeriphClkInit.Adc12ClockSelection = RCC_ADC12PLLCLK_DIV1;
  PeriphClkInit.Tim15ClockSelection = RCC_TIM15CLK_HCLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */



/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void) // @suppress("Name convention for function")
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */

	pr("Error_Handler\n\r");
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{ 
  /* USER CODE BEGIN 6 */
	pr("assert_failed\n\r");
  /* User can add his own implementation to report the file name and line number,
     text: print("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
