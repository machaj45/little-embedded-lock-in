\documentclass[11pt,a4paper]{report}
\usepackage[cp1250]{inputenc}
\usepackage[czech]{babel}
\usepackage[T1]{fontenc}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{fancyhdr}
\usepackage{menukeys}
\usepackage{subcaption}
\usepackage{mathtools}
\usepackage{circuitikz}
\usepackage{graphicx}
\usepackage{epstopdf}
\usepackage{subcaption}
\usepackage{float}
\usepackage{circuitikz}
\usetikzlibrary{shapes.multipart}
\usetikzlibrary{shapes}
\usepackage[colorlinks = true,
            linkcolor = blue,
            urlcolor  = blue,
            citecolor = blue,
            anchorcolor = blue]{hyperref}
\usepackage[colorlinks = true,linkcolor = blue,urlcolor  = blue,citecolor = blue,anchorcolor = blue]{hyperref}
\usepackage[left=1.5cm,right=1.5cm,top=3cm,bottom=1.5cm,headheight=1.5cm]{geometry}
\usetikzlibrary{patterns}
\author{Jan Machálek}
\ctikzset{resistor = european}
\usepackage[figurename=obr.]{caption}
\usepackage{textcomp}
\usetikzlibrary{shapes,arrows}



\newcommand{\pu}[1]{\textcolor{purple}{#1}}
\newcommand{\re}[1]{\textcolor{red}{#1}}

\makeatletter %new code
\pgfdeclarepatternformonly[\LineSpace,\tikz@pattern@color]{my north east lines}{\pgfqpoint{-1pt}{-1pt}}{\pgfqpoint{\LineSpace}{\LineSpace}}{\pgfqpoint{\LineSpace}{\LineSpace}}%
{
    \pgfsetcolor{\tikz@pattern@color} %new code
    \pgfsetlinewidth{0.4pt}
    \pgfpathmoveto{\pgfqpoint{0pt}{0pt}}
    \pgfpathlineto{\pgfqpoint{\LineSpace + 0.1pt}{\LineSpace + 0.1pt}}
    \pgfusepath{stroke}
}
\makeatother %new code
\newdimen\LineSpace
\tikzset{
    line space/.code={\LineSpace=#1},
    line space=3pt
}
\DeclareMathOperator{\arctantwo}{arctan2}



\begin{document}
\tikzset{%
  block/.style    = {draw, thick, rectangle, minimum height = 3em,
    minimum width = 3em},
  sum/.style      = {draw, circle, node distance = 2cm}, % Adder
  input/.style    = {coordinate}, % Input
  output/.style   = {coordinate} % Output
}
% Defining string as labels of certain blocks.
\newcommand{\suma}{\Large$+$}
\newcommand{\inte}{$\displaystyle \int$}
\newcommand{\derv}{\huge$\frac{d}{dt}$}
\fancypagestyle{logo}{
\fancyhf{}
\fancyhead[CE,CO]{\includegraphics[scale=0.15]{pic/ctu_logo_blue.pdf}}
\lhead{ \fancyplain{}{Bc. Jan Machálek} }
\rhead{ \fancyplain{}{\today} }
\rfoot{ \fancyplain{}{\thepage} }
\fancyfoot[L]{Bc. Jan Machálek}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\today}
\renewcommand{\footrulewidth}{0.4pt}
}
\pagestyle{logo}
\renewcommand{\headrulewidth}{0.4pt}
\title{Návod pro používání lock-in zesilovaèe}
\maketitle
\chapter {Úvod}
Tento virtuální pøístroj je vyvíjen v rámci mé diplomové práce. Realizuje lock-in zesilovaè, jehož fungování je blíže popsáno v mé diplomové práci. Tento návod seznamuje s virtuálním pøístrojem a jak s ním mìøit a co dìlat v pøípadì chybového stavu. V rámci tohoto návodu se uživatel dozví, jak nastavit a mìøit pomocí tohoto nástroje v ruèním a také v automatizovaném mìøení. Uživatel bude seznámen s pøipojováním pøístroje do obvodu. \\
p.s. Prosím o nahlášení všech chyb a zpùsobu jejich vyvolání, které naleznete na adresu machaj45@fel.cvut.cz pøedem dìkuji za pomoc.
\newpage
\section{Instalace aplikace a nahrání firmwareu}
Pro spuštìní pøístroje je nutné nejprve nahrát lock-in.bin do Nucleo-F303RE. Poté spustit aplikaci lock-in.exe. V pøípadì, že antivirus zakáže spouštìní programu, pak je nutné na chvíli zakázat antivirus. Napøíklad Avast program provìøí a poté již funguje dobøe. Jestliže není pøístroj pøipojen nastane následující situace:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/conn}
\caption{Stav aplikace nepøipojeno.}
\label{nep}
\end{figure}
Kde je dobré se ujistit, že èíslo v názvu okna se zvyšuje a není stále pouze jedna. Možná øešení problému vypnout zapnout aplikaci v pc nebo zkusit jiný USB port.
\newpage
\section{Pøehled grafické rozhraní poèítaèové aplikace}
Pøístroj má dva generátory, které se ovládají pomocí grafických elementù až do nápisu sample per period. Pro generované výstupy se dá nastavovat amplituda, offset, frekvence.  \\Mìøící èást je poté organizovaná pomocí poètu vzorkù na periodu to znamená kolik vzorkù se odebere za jednu periodu specifikované pomocí \textbf{Samples per period}.\\
Další ovládací prvky jsou v dolní èásti, které umožòují samotné mìøení.  \\
Tlaèítko \textbf{Continous} mìøí a vyèítá data z kit dokud se tato akce neukonèí opìtovným kliknutím na tlaèítko \textbf{Continous} poté dobìhne poslední mìøení. \\
Tlaèítko \textbf{Single} provede jedno mìøení. Pøed stiskem Tlaèítka \textbf{Continous} nebo \textbf{Single} musí být nastaven generátor na kanálu 1 a také musí být zvolen poèet vzorkù na periodu. \\
Tlaèítko \textbf{Toggle to Square} pøepne oba generátoru do obdélníkového prùbìhu a opìtovnì nastaví kanál 1. Následnì se popis tohoto tlaèítka zmìní na \textbf{Toggle to Sin} pomocí, kterého se pøepne aplikace do sinusového modu. \\
Tlaèítko \textbf{Draw data} vykresluje právì naètená data pro kontrolu správnosti namìøených dat.\\
Tlaèítko \textbf{Automatic measrument} provádí automatické mìøení pro rùzné frekvence které jsou zadané v souboru \textbf{frec.cvs}, který se nachází ve složce kde byla spuštìna aplikace lock-in.
\newpage
\section{Spuštìní virtuálního pøístroje}
Po pøipojení nuclea s nahraným firmwarem a spuštìní aplikace by mìlo vypadat:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/conn2}
\caption{Stav aplikace pøipojeno.}
\end{figure}
Hlavní informace se nachází ve jménì okna a to, že jste pøipojeni k nucleu na comportu X. Jestliže se tak stalo, vše je v poøádku. Mohlo by se však stát, že  aplikace uvízla ve stavu \ref{nep}, tento stav se dá zmìnit pomocí restartovaní aplikace nebo zmìny USB do kterého je nucleo pøipojeno nebo kombinací obojího. Jestliže je vše v poøádku, aplikace vás informuje, že jste pøipojeni. 
\newpage
\subsection{Nastavení generátoru pro kanál 1}
Pro testovací úèely mùžeme nechat nastavení tak, jak je a nahrát je všechny do nuclea pomocí tlaèítka Set Up Generator 1. Tato akce nastaví všechna potøebná nastavení pro první kanál generátoru, který je nastaven na výstup nuclea \pu{A2}. Jestliže nastavení probìhlo úspìšnì, mìli bychom v názvu okna dostat následující informaci jako poslední "Send 310, Received 310". Jestliže jste nezmìnili offset výsledek by mìl vypadat takto:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/gen1}
\caption{Stav aplikace generátor nastaven.}
\end{figure}
\subsection{Nastavení vzorkù na periodu}
Po nastavení generátoru je potøeba nastavit poèet vzorkù na periodu. Toto nastavení je tøeba provádìt až po nastavení generátoru èíslo jedna. Aby jsem dostali správnou informaci zobrazenou nad výbìrem poètu vzorku na periodu. Informace zobrazené na obrázku \ref{ssp} jsou poèet vzorkù na periodu, vzorkovací frekvence, s èas který je potøeba na odebrání jednoho vzorku pomocí obvodu sample and hold pro pøevodník.
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/ssp}

\caption{Zobrazení informace pro uživatele po nastavení generátoru a poètu vzorkù na periodu.}
\label{ssp}
\end{figure}
\newpage
\subsection{První mìøení pomocí virtuálního pøístroje}
Po nastavení generátoru a vzorkù na periodu mùžeme provádìt jednotlivá ruèní mìøení pomocí tlaèítka \textbf{Continous} a \textbf{Single} poté se nad grafem objeví fázový posun, zesílení , X, Y $U_2$ a délka èasového záznamu pro sinusový mod, v pøípade obdélníkového prùbìhu se nad grafem objeví støední hodnota usmìrnìného napìtí $U_2$, smìrodatná odchylka a délka èasového záznamu.  Takový stav po úspìšném vyètení dat by mìl vypadat tøeba takto:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/obd}
\caption{Stav aplikace naètení dat pro obdélníkový prùbìh.}
\end{figure}
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/sin}
\caption{Stav aplikace naètení dat pro sinusový prùbìh.}
\end{figure}
Pro kontrolu mùžeme pomocí tlaèítka \textbf{Draw data} vykreslit data do grafu a pøesvìdèit se, že mìøíme to co chceme. Zde mùžeme zjistit napøíklad zdali využíváme sinusový nebo obdélníkový prùbìh:
\begin{figure}[H]
\centering
\includegraphics[width=.5\textwidth]{pic/sincheck}
\caption{Kontrola navzorkovaných dat (dìliè napìtí), generátor nastaven pro sinusový výstup.}
\end{figure}
\begin{figure}[H]
\centering
\includegraphics[width=.5\textwidth]{pic/obdcheck}
\caption{Kontrola navzorkovaných dat (dìliè napìtí), generátor nastaven pro obdélníkový výstup.}
\end{figure}
\newpage
\section{Automatizované mìøení pomocí virtuálního pøístroje}
Pro automatizované mìøení si staèí pøipravit seznam mìøených frekvencí do souboru "freq.cvs" ~poté nastavit generátor  offset, amplitudu, tvar generovaného signálu a poèet vzorkù na periodu. Stiskem tlaèítka \textbf{Automatic Measurment} vyèkat, dokud se nezobrazí na dolním popisku nad grafem \textbf{Done}.
Když se tak, stane mùžeme se na data podívat do souboru data.csv, která se nacházejí ve složce kde je aplikace.
\section{Pøechod do modu øízený usmìròovaè.}
Po spuštìní aplikace se virtuální pøístroj nastaví do režimu kde generuje sinusový prùbìh a vypoèítává fázový posun a zesílení. V pøípadì že chceme používat pøístroj jako øízený usmìròovaè použijeme tlaèítko dole uprostøed \textbf{Toggle to Square}. Po pøepnutí do modu "Square"~ se generuje na výstupu \pu{A2} obdélníkový prùbìh s 50\% støídou. Následnì je referenèní signál mìøený pomocí vstupu \pu{A5} zmìnìn na hodnotu +1 pakliže je vìtší než jeho støední hodnota a -1 jestliže je menší než jeho støední hodnota. Výsledný usmìrnìný prùbìh je zobrazen na obrázku \ref{usm}. Hodnota X potom reprezentuje hodnotu støední hodnoty usmìrnìného signálu. V tomto režimu není možnost používat automatizovaného mìøení. Používejte proto pouze tlaèítka \textbf{Continous} a \textbf{Single}. Generátoru se dá stále nastavovat amplituda, offset a frekvence.
\begin{figure}[H]
\centering
\includegraphics[width=.8\textwidth]{pic/usm}
\caption{Výsledky mìøené pomocí virtuálního pøístroje v režimu øízený usmìròovaè.}
\label{usm}
\end{figure}
Na obrázku \ref{usm} jsou prùbìhy kde èervenì je reprezentován signál namìøený na vstupu \pu{A4} tedy výstup z mìøeného obvodu, zelenì je reprezentován signál mìøený na vstupu \pu{A5} tedy reference zmìnìná na hodnoty +1 a -1. Modrou barvou je reprezentován signál který vznikne po pro-násobení tìchto dvou signálù.
Pøepnutí zpìt do modu kdy je generován sinusový prùbìh se provede pomocí stejného tlaèítka \textbf{Toggle to sin} nebo restartováním aplikace.
\newpage
\section{Zapojení virtuálního pøístroje do mìøených obvodù }
Pro mìøení obvodových vlastností je potøeba správnì pøipojit lock-in do obvodu. Tento pøístroj používá 
výstupu \pu{A2} a vstupy \pu{A4} a \pu{A5}. Kde \pu{A2} je generátor, který je možné nastavit pomocí tlaèítka S\textbf{et up Generator 1}. Dva vstupy jsou zde pro mìøení, jak referenèního signálu, tak pro mìøený výstupu z obvodu. Vstup pro referenci je vstup \pu{A5} a vstup pro výstup z obvodu je vstup \pu{A4}.\\
Na schématech \ref{delic} a \ref{rc} jsou zobrazena možná zapojení dìlièe z reálných odporù a RC èlánku. Na obrázcích  \ref{fig:pinout} a \ref{fig:obrdiod} je zobrazena lokace pinu \pu{A2}, \pu{A4}, \pu{A5}.
\begin{figure}[H]
\begin{subfigure}{.5\textwidth}
\centering
\begin{circuitikz}
\draw (-1,2)node [odiamondpole,label=\pu{A2}] {}(-1,2)--(0,2);
\draw (1,2)node [odiamondpole,label=\pu{A5}] {}(1,2)--(0,2);
\draw (1,0)node [odiamondpole,label=\pu{A4}] {}(1,0)--(0,0);
\draw (0,2)to[R=$R_1$,*-*](0,0) ;
\draw (0,0)to[R=$R_2$](0,-2) ;
\draw (0,-2)node[ground]{};
\end{circuitikz}
\caption{Schéma pro zapojení generátoru a lock-in zesilovaèe pro mìøení dìlièe, kde \pu{A2} je generátor,\pu{A5} je mìøení referenèního signálu a  \pu{A4} je mìøení výstupu z mìøeného obvodu.}
\label{delic}
\end{subfigure}
\begin{subfigure}{.4\textwidth}
\centering
\begin{circuitikz}
\draw (-1,2)node [odiamondpole,label=\pu{A2}] {}(-1,2)--(0,2);
\draw (1,2)node [odiamondpole,label=\pu{A5}] {}(1,2)--(0,2);
\draw (1,0)node [odiamondpole,label=\pu{A4}] {}(1,0)--(0,0);
\draw (0,2)to[R=$R$,*-*](0,0) ;
\draw (0,0)to[C=$C$](0,-2) ;
\draw (0,-2)--(0,-2.4);
\draw (0,-2.4)node[ground]{};
\end{circuitikz}
\caption{Schéma pro zapojení generátoru a lock-in zesilovaèe pro mìøení RC èlánku, kde \pu{A2} je generátor,\pu{A5} je mìøení referenèního signálu a  \pu{A4} je mìøení výstupu z mìøeného obvodu.}
\label{rc}
\end{subfigure}
\end{figure}
\begin{figure}[H]
\centering
\subcaptionbox{Nucleo F303RE.\label{fig:obrdiod}}%
  [.45\textwidth]{
\includegraphics[page=1,trim=7.7cm 7cm 6cm 14.4cm,clip,scale=0.9]{pic/pins.pdf} 
}
\subcaptionbox{Popis pinù kitu Nucleo F303RE .\label{fig:pinout}}%
  [.45\textwidth]{
  \centering
\includegraphics[page=31,trim=7.8cm 19.2cm 5.8cm 3.7cm,clip,scale=1.0]{pic/pins.pdf}  
\hfill
}
\caption{Nucleo F303RE a popis pinù.}
\end{figure}
\end{document} 