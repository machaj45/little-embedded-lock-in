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
\author{Jan Mach�lek}
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
\lhead{ \fancyplain{}{Bc. Jan Mach�lek} }
\rhead{ \fancyplain{}{\today} }
\rfoot{ \fancyplain{}{\thepage} }
\fancyfoot[L]{Bc. Jan Mach�lek}
\fancyfoot[C]{\thepage}
\fancyfoot[R]{\today}
\renewcommand{\footrulewidth}{0.4pt}
}
\pagestyle{logo}
\renewcommand{\headrulewidth}{0.4pt}
\title{N�vod pro pou��v�n� lock-in zesilova�e}
\maketitle
\chapter {�vod}
Tento virtu�ln� p��stroj je vyv�jen v r�mci m� diplomov� pr�ce. Realizuje lock-in zesilova�, jeho� fungov�n� je bl�e pops�no v m� diplomov� pr�ci. Tento n�vod seznamuje s virtu�ln�m p��strojem a jak s n�m m��it a co d�lat v p��pad� chybov�ho stavu. V r�mci tohoto n�vodu se u�ivatel dozv�, jak nastavit a m��it pomoc� tohoto n�stroje v ru�n�m a tak� v automatizovan�m m��en�. U�ivatel bude sezn�men s p�ipojov�n�m p��stroje do obvodu. \\
p.s. Pros�m o nahl�en� v�ech chyb a zp�sobu jejich vyvol�n�, kter� naleznete na adresu machaj45@fel.cvut.cz p�edem d�kuji za pomoc.
\newpage
\section{Instalace aplikace a nahr�n� firmwareu}
Pro spu�t�n� p��stroje je nutn� nejprve nahr�t lock-in.bin do Nucleo-F303RE. Pot� spustit aplikaci lock-in.exe. V p��pad�, �e antivirus zak�e spou�t�n� programu, pak je nutn� na chv�li zak�zat antivirus. Nap��klad Avast program prov��� a pot� ji� funguje dob�e. Jestli�e nen� p��stroj p�ipojen nastane n�sleduj�c� situace:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/conn}
\caption{Stav aplikace nep�ipojeno.}
\label{nep}
\end{figure}
Kde je dobr� se ujistit, �e ��slo v n�zvu okna se zvy�uje a nen� st�le pouze jedna. Mo�n� �e�en� probl�mu vypnout zapnout aplikaci v pc nebo zkusit jin� USB port.
\newpage
\section{P�ehled grafick� rozhran� po��ta�ov� aplikace}
P��stroj m� dva gener�tory, kter� se ovl�daj� pomoc� grafick�ch element� a� do n�pisu sample per period. Pro generovan� v�stupy se d� nastavovat amplituda, offset, frekvence.  \\M���c� ��st je pot� organizovan� pomoc� po�tu vzork� na periodu to znamen� kolik vzork� se odebere za jednu periodu specifikovan� pomoc� \textbf{Samples per period}.\\
Dal�� ovl�dac� prvky jsou v doln� ��sti, kter� umo��uj� samotn� m��en�.  \\
Tla��tko \textbf{Continous} m��� a vy��t� data z kit dokud se tato akce neukon�� op�tovn�m kliknut�m na tla��tko \textbf{Continous} pot� dob�hne posledn� m��en�. \\
Tla��tko \textbf{Single} provede jedno m��en�. P�ed stiskem Tla��tka \textbf{Continous} nebo \textbf{Single} mus� b�t nastaven gener�tor na kan�lu 1 a tak� mus� b�t zvolen po�et vzork� na periodu. \\
Tla��tko \textbf{Toggle to Square} p�epne oba gener�toru do obd�ln�kov�ho pr�b�hu a op�tovn� nastav� kan�l 1. N�sledn� se popis tohoto tla��tka zm�n� na \textbf{Toggle to Sin} pomoc�, kter�ho se p�epne aplikace do sinusov�ho modu. \\
Tla��tko \textbf{Draw data} vykresluje pr�v� na�ten� data pro kontrolu spr�vnosti nam��en�ch dat.\\
Tla��tko \textbf{Automatic measrument} prov�d� automatick� m��en� pro r�zn� frekvence kter� jsou zadan� v souboru \textbf{frec.cvs}, kter� se nach�z� ve slo�ce kde byla spu�t�na aplikace lock-in.
\newpage
\section{Spu�t�n� virtu�ln�ho p��stroje}
Po p�ipojen� nuclea s nahran�m firmwarem a spu�t�n� aplikace by m�lo vypadat:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/conn2}
\caption{Stav aplikace p�ipojeno.}
\end{figure}
Hlavn� informace se nach�z� ve jm�n� okna a to, �e jste p�ipojeni k nucleu na comportu X. Jestli�e se tak stalo, v�e je v po��dku. Mohlo by se v�ak st�t, �e  aplikace uv�zla ve stavu \ref{nep}, tento stav se d� zm�nit pomoc� restartovan� aplikace nebo zm�ny USB do kter�ho je nucleo p�ipojeno nebo kombinac� oboj�ho. Jestli�e je v�e v po��dku, aplikace v�s informuje, �e jste p�ipojeni. 
\newpage
\subsection{Nastaven� gener�toru pro kan�l 1}
Pro testovac� ��ely m��eme nechat nastaven� tak, jak je a nahr�t je v�echny do nuclea pomoc� tla��tka Set Up Generator 1. Tato akce nastav� v�echna pot�ebn� nastaven� pro prvn� kan�l gener�toru, kter� je nastaven na v�stup nuclea \pu{A2}. Jestli�e nastaven� prob�hlo �sp�n�, m�li bychom v n�zvu okna dostat n�sleduj�c� informaci jako posledn� "Send 310, Received 310". Jestli�e jste nezm�nili offset v�sledek by m�l vypadat takto:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/gen1}
\caption{Stav aplikace gener�tor nastaven.}
\end{figure}
\subsection{Nastaven� vzork� na periodu}
Po nastaven� gener�toru je pot�eba nastavit po�et vzork� na periodu. Toto nastaven� je t�eba prov�d�t a� po nastaven� gener�toru ��slo jedna. Aby jsem dostali spr�vnou informaci zobrazenou nad v�b�rem po�tu vzorku na periodu. Informace zobrazen� na obr�zku \ref{ssp} jsou po�et vzork� na periodu, vzorkovac� frekvence, s �as kter� je pot�eba na odebr�n� jednoho vzorku pomoc� obvodu sample and hold pro p�evodn�k.
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/ssp}

\caption{Zobrazen� informace pro u�ivatele po nastaven� gener�toru a po�tu vzork� na periodu.}
\label{ssp}
\end{figure}
\newpage
\subsection{Prvn� m��en� pomoc� virtu�ln�ho p��stroje}
Po nastaven� gener�toru a vzork� na periodu m��eme prov�d�t jednotliv� ru�n� m��en� pomoc� tla��tka \textbf{Continous} a \textbf{Single} pot� se nad grafem objev� f�zov� posun, zes�len� , X, Y $U_2$ a d�lka �asov�ho z�znamu pro sinusov� mod, v p��pade obd�ln�kov�ho pr�b�hu se nad grafem objev� st�edn� hodnota usm�rn�n�ho nap�t� $U_2$, sm�rodatn� odchylka a d�lka �asov�ho z�znamu.  Takov� stav po �sp�n�m vy�ten� dat by m�l vypadat t�eba takto:
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/obd}
\caption{Stav aplikace na�ten� dat pro obd�ln�kov� pr�b�h.}
\end{figure}
\begin{figure}[H]
\centering
\includegraphics[width=.7\textwidth]{pic/sin}
\caption{Stav aplikace na�ten� dat pro sinusov� pr�b�h.}
\end{figure}
Pro kontrolu m��eme pomoc� tla��tka \textbf{Draw data} vykreslit data do grafu a p�esv�d�it se, �e m���me to co chceme. Zde m��eme zjistit nap��klad zdali vyu��v�me sinusov� nebo obd�ln�kov� pr�b�h:
\begin{figure}[H]
\centering
\includegraphics[width=.5\textwidth]{pic/sincheck}
\caption{Kontrola navzorkovan�ch dat (d�li� nap�t�), gener�tor nastaven pro sinusov� v�stup.}
\end{figure}
\begin{figure}[H]
\centering
\includegraphics[width=.5\textwidth]{pic/obdcheck}
\caption{Kontrola navzorkovan�ch dat (d�li� nap�t�), gener�tor nastaven pro obd�ln�kov� v�stup.}
\end{figure}
\newpage
\section{Automatizovan� m��en� pomoc� virtu�ln�ho p��stroje}
Pro automatizovan� m��en� si sta�� p�ipravit seznam m��en�ch frekvenc� do souboru "freq.cvs" ~pot� nastavit gener�tor  offset, amplitudu, tvar generovan�ho sign�lu a po�et vzork� na periodu. Stiskem tla��tka \textbf{Automatic Measurment} vy�kat, dokud se nezobraz� na doln�m popisku nad grafem \textbf{Done}.
Kdy� se tak, stane m��eme se na data pod�vat do souboru data.csv, kter� se nach�zej� ve slo�ce kde je aplikace.
\section{P�echod do modu ��zen� usm�r�ova�.}
Po spu�t�n� aplikace se virtu�ln� p��stroj nastav� do re�imu kde generuje sinusov� pr�b�h a vypo��t�v� f�zov� posun a zes�len�. V p��pad� �e chceme pou��vat p��stroj jako ��zen� usm�r�ova� pou�ijeme tla��tko dole uprost�ed \textbf{Toggle to Square}. Po p�epnut� do modu "Square"~ se generuje na v�stupu \pu{A2} obd�ln�kov� pr�b�h s 50\% st��dou. N�sledn� je referen�n� sign�l m��en� pomoc� vstupu \pu{A5} zm�n�n na hodnotu +1 pakli�e je v�t�� ne� jeho st�edn� hodnota a -1 jestli�e je men�� ne� jeho st�edn� hodnota. V�sledn� usm�rn�n� pr�b�h je zobrazen na obr�zku \ref{usm}. Hodnota X potom reprezentuje hodnotu st�edn� hodnoty usm�rn�n�ho sign�lu. V tomto re�imu nen� mo�nost pou��vat automatizovan�ho m��en�. Pou��vejte proto pouze tla��tka \textbf{Continous} a \textbf{Single}. Gener�toru se d� st�le nastavovat amplituda, offset a frekvence.
\begin{figure}[H]
\centering
\includegraphics[width=.8\textwidth]{pic/usm}
\caption{V�sledky m��en� pomoc� virtu�ln�ho p��stroje v re�imu ��zen� usm�r�ova�.}
\label{usm}
\end{figure}
Na obr�zku \ref{usm} jsou pr�b�hy kde �erven� je reprezentov�n sign�l nam��en� na vstupu \pu{A4} tedy v�stup z m��en�ho obvodu, zelen� je reprezentov�n sign�l m��en� na vstupu \pu{A5} tedy reference zm�n�n� na hodnoty +1 a -1. Modrou barvou je reprezentov�n sign�l kter� vznikne po pro-n�soben� t�chto dvou sign�l�.
P�epnut� zp�t do modu kdy je generov�n sinusov� pr�b�h se provede pomoc� stejn�ho tla��tka \textbf{Toggle to sin} nebo restartov�n�m aplikace.
\newpage
\section{Zapojen� virtu�ln�ho p��stroje do m��en�ch obvod� }
Pro m��en� obvodov�ch vlastnost� je pot�eba spr�vn� p�ipojit lock-in do obvodu. Tento p��stroj pou��v� 
v�stupu \pu{A2} a vstupy \pu{A4} a \pu{A5}. Kde \pu{A2} je gener�tor, kter� je mo�n� nastavit pomoc� tla��tka S\textbf{et up Generator 1}. Dva vstupy jsou zde pro m��en�, jak referen�n�ho sign�lu, tak pro m��en� v�stupu z obvodu. Vstup pro referenci je vstup \pu{A5} a vstup pro v�stup z obvodu je vstup \pu{A4}.\\
Na sch�matech \ref{delic} a \ref{rc} jsou zobrazena mo�n� zapojen� d�li�e z re�ln�ch odpor� a RC �l�nku. Na obr�zc�ch  \ref{fig:pinout} a \ref{fig:obrdiod} je zobrazena lokace pinu \pu{A2}, \pu{A4}, \pu{A5}.
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
\caption{Sch�ma pro zapojen� gener�toru a lock-in zesilova�e pro m��en� d�li�e, kde \pu{A2} je gener�tor,\pu{A5} je m��en� referen�n�ho sign�lu a  \pu{A4} je m��en� v�stupu z m��en�ho obvodu.}
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
\caption{Sch�ma pro zapojen� gener�toru a lock-in zesilova�e pro m��en� RC �l�nku, kde \pu{A2} je gener�tor,\pu{A5} je m��en� referen�n�ho sign�lu a  \pu{A4} je m��en� v�stupu z m��en�ho obvodu.}
\label{rc}
\end{subfigure}
\end{figure}
\begin{figure}[H]
\centering
\subcaptionbox{Nucleo F303RE.\label{fig:obrdiod}}%
  [.45\textwidth]{
\includegraphics[page=1,trim=7.7cm 7cm 6cm 14.4cm,clip,scale=0.9]{pic/pins.pdf} 
}
\subcaptionbox{Popis pin� kitu Nucleo F303RE .\label{fig:pinout}}%
  [.45\textwidth]{
  \centering
\includegraphics[page=31,trim=7.8cm 19.2cm 5.8cm 3.7cm,clip,scale=1.0]{pic/pins.pdf}  
\hfill
}
\caption{Nucleo F303RE a popis pin�.}
\end{figure}
\end{document} 