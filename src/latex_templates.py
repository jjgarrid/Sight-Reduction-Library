"""
LaTeX Templates for Celestial Navigation Problems and Almanac Pages

This module defines LaTeX templates for generating professional-looking 
celestial navigation worksheets and almanac pages.
"""

# Main template for a sight reduction problem worksheet
SIGHT_REDUCTION_PROBLEM_TEMPLATE = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{array}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{amsmath}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{titlesec}

% Page setup
\geometry{margin=1in}
\pagestyle{fancy}
\fancyhf{}
\rhead{Celestial Navigation Practice}
\lhead{Sight Reduction Worksheet}
\rfoot{\thepage}

% Custom commands
\newcommand{\sightentry}[2]{\textbf{#1:} & #2 \\}
\newcommand{\tabitem}{~~\llap{\textbullet}~~}

\titleformat{\section}
{\normalfont\Large\bfseries}{\thesection}{1em}{}

\begin{document}

\begin{center}
{\Huge\textbf{SIGHT REDUCTION WORKSHEET}} \\
\vspace{0.5cm}
{\large Celestial Navigation Practice Problem}
\end{center}

\vspace{1cm}

\section*{Observation Details}

\begin{tabular}{>{\bfseries}lp{10cm}}
Celestial Body: & {{%(celestial_body_name)s}}{{%(limb_text)s}} \\
Observation Time (UTC): & {{%(observation_time)s}} \\
Observed Sextant Altitude: & {{%(observed_altitude)s}} \\
\end{tabular}

\vspace{1cm}

\section*{Environmental Conditions}

\begin{tabular}{>{\bfseries}lp{10cm}}
Temperature: & {{%(temperature)s}} \textcelsius \\
Atmospheric Pressure: & {{%(pressure)s}} hPa \\
Observer Height: & {{%(observer_height)s}} meters \\
\end{tabular}

\vspace{1cm}

\section*{Assumed Position}

\begin{tabular}{>{\bfseries}lp{10cm}}
Latitude: & {{%(assumed_lat)s}} \\
Longitude: & {{%(assumed_lon)s}} \\
\end{tabular}

\vspace{1cm}

\section*{Instrument Parameters}

\begin{tabular}{>{\bfseries}lp{10cm}}
Instrument Error: & {{%(instrument_error)s}} \\
Index Error: & {{%(index_error)s}} \\
Personal Error: & {{%(personal_error)s}} \\
\end{tabular}

\vspace{1cm}

\section*{Task}

Using the sight reduction method of your choice, calculate:
\begin{enumerate}
    \item The computed altitude ($H_c$) and azimuth ($Z_n$) for the assumed position
    \item The intercept ($a$) and its direction (Toward/Away from the celestial body)
    \item Plot the line of position on a plotting sheet
\end{enumerate}

\vspace{1cm}

\begin{tikzpicture}[scale=0.8]
  \draw[step=1cm,gray,very thin] (0,0) grid (12,8);
  \draw[thick] (0,0) rectangle (12,8);
  \node at (6,7.5) {\textbf{PLOTTING AREA}};
  \node at (6,7) {Use this space to plot your line of position};
\end{tikzpicture}

\vspace{1cm}

\section*{Solution Space}

\vspace{8cm} % Leave space for calculations

\newpage

% Answer Key (only appears in solution version)
%(answer_key)s

\end{document}
"""

# Template for answer key
ANSWER_KEY_TEMPLATE = r"""
\section*{Answer Key}

\begin{tabular}{>{\bfseries}lp{10cm}}
Actual Position: & %(actual_lat)s, %(actual_lon)s \\
Computed Altitude ($H_c$): & %(computed_altitude)s \\
Azimuth ($Z_n$): & %(azimuth)s \\
Intercept ($a$): & %(intercept)s %(intercept_direction)s \\
\end{tabular}

\vspace{1cm}

\textbf{Steps to Solution:}
\begin{enumerate}
    \item Calculate LHA = GHA - Assumed Longitude
    \item Enter sight reduction tables with LHA, Assumed Latitude, and Declination
    \item Extract $H_c$ and $Z$
    \item Convert $Z$ to $Z_n$ based on hemisphere and LHA
    \item Calculate intercept: $a = H_o - H_c$
\end{enumerate}
"""

# Template for almanac pages
ALMANAC_PAGE_TEMPLATE = r"""
\documentclass[10pt,a4paper,twocolumn]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{array}
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{siunitx}
\usepackage{multicol}

% Page setup
\geometry{margin=0.75in}
\pagestyle{fancy}
\fancyhf{}
\rhead{Nautical Almanac - %(date)s}
\lhead{Celestial Body: %(celestial_body_name)s}
\rfoot{\thepage}

\begin{document}

\begin{center}
{\Large\textbf{NAUTICAL ALMANAC}} \\
\vspace{0.2cm}
{\large %(celestial_body_name)s - %(date)s} \\
\end{center}

\vspace{0.5cm}

\section*{Hourly Data}

\begin{center}
\begin{longtable}{|c|c|c|c|c|}
\hline
\textbf{Time} & \textbf{GHA} & \textbf{Dec} & \textbf{SD} & \textbf{HP} \\
\hline
\endfirsthead
\hline
\textbf{Time} & \textbf{GHA} & \textbf{Dec} & \textbf{SD} & \textbf{HP} \\
\hline
\endhead
\hline
\endfoot
\hline
\endlastfoot
%(hourly_data_rows)s
\end{longtable}
\end{center}

\vspace{1cm}

\section*{Additional Information}

\begin{tabular}{>{\bfseries}lp{8cm}}
Semi-Diameter: & %(semi_diameter)s \\
Horizontal Parallax: & %(horizontal_parallax)s \\
Magnitude: & %(magnitude)s \\
\end{tabular}

\vspace{1cm}

\textbf{Notes:}
\begin{itemize}
    \item GHA = Greenwich Hour Angle
    \item Dec = Declination
    \item SD = Semi-Diameter
    \item HP = Horizontal Parallax
\end{itemize}

\end{document}
"""

# Template for multiple sight reduction problems
MULTIPLE_SIGHT_REDUCTION_TEMPLATE = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{array}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{longtable}
\usepackage{amsmath}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{tikz}

% Page setup
\geometry{margin=1in}
\pagestyle{fancy}
\fancyhf{}
\rhead{Celestial Navigation Fix}
\lhead{Multiple Sight Reduction}
\rfoot{\thepage}

\begin{document}

\begin{center}
{\Huge\textbf{CELESTIAL NAVIGATION FIX}} \\
\vspace{0.5cm}
{\large Multiple Sight Reduction Problem Set}
\end{center}

\vspace{1cm}

\textbf{Date:} %(date)s \hfill \textbf{Time Window:} %(time_window)s \\
\textbf{Vessel Speed:} %(vessel_speed)s knots \hfill \textbf{Course:} %(vessel_course)s\textdegree

\vspace{1cm}

\section*{Observations}

\begin{center}
\begin{longtable}{|c|c|c|c|c|c|}
\hline
\textbf{Body} & \textbf{Time} & \textbf{Sextant Alt.} & \textbf{Temp.} & \textbf{Pressure} & \textbf{Observer Height} \\
\hline
\endfirsthead
\hline
\textbf{Body} & \textbf{Time} & \textbf{Sextant Alt.} & \textbf{Temp.} & \textbf{Pressure} & \textbf{Observer Height} \\
\hline
\endhead
\hline
\endfoot
\hline
\endlastfoot
%(observations_table)s
\end{longtable}
\end{center}

\vspace{1cm}

\section*{Task}

Using the sight reduction method of your choice, calculate:
\begin{enumerate}
    \item The computed altitude ($H_c$) and azimuth ($Z_n$) for each observation
    \item The intercept ($a$) and its direction for each observation
    \item Plot all lines of position and determine the fix
\end{enumerate}

\vspace{1cm}

\begin{center}
\textbf{FIX POSITION:} \framebox(300,20){\rule{0pt}{10pt}\hspace{3cm}} \\
\end{center}

\vspace{1cm}

\begin{tikzpicture}[scale=0.6]
  \draw[step=1cm,gray,very thin] (0,0) grid (20,14);
  \draw[thick] (0,0) rectangle (20,14);
  \node at (10,13.5) {\textbf{PLOTTING AREA}};
  \node at (10,12.5) {Use this space to plot all lines of position and determine the fix};
\end{tikzpicture}

\vspace{1cm}

\section*{Solution Space}

\vspace{8cm} % Leave space for calculations

% Answer Key (only appears in solution version)
%(answer_key)s

\end{document}
"""

# Template for sight reduction booklet
SIGHT_REDUCTION_BOOKLET_TEMPLATE = r"""
\documentclass[12pt,a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{geometry}
\usepackage{fancyhdr}
\usepackage{array}
\usepackage{booktabs}
\usepackage{multirow}
\usepackage{amsmath}
\usepackage{siunitx}
\usepackage{graphicx}
\usepackage{tikz}
\usepackage{titlesec}
\usepackage{longtable}
\usepackage{float}

% Page setup
\geometry{margin=1in}
\pagestyle{fancy}
\fancyhf{}
\rhead{Celestial Navigation Practice}
\lhead{Sight Reduction Booklet}
\rfoot{\thepage}

% Custom commands
\newcommand{\sightentry}[2]{\textbf{#1:} & #2 \\}
\newcommand{\tabitem}{~~\llap{\textbullet}~~}

\titleformat{\section}
{\normalfont\Large\bfseries}{\thesection}{1em}{}

\begin{document}

% Exercise Page
\begin{center}
{\Huge\textbf{SIGHT REDUCTION BOOKLET}} \\
\vspace{0.5cm}
{\large Celestial Navigation Practice Problems}
\end{center}

\section*{Exercise Page}

\subsection*{Observation Details}

\begin{tabular}{>{\bfseries}lp{10cm}}
Celestial Body: & %(celestial_body_name)s%(limb_text)s \\
Observation Time (UTC): & %(observation_time)s \\
Observed Sextant Altitude: & %(observed_altitude)s \\
\end{tabular}

\vspace{1cm}

\subsection*{Environmental Conditions}

\begin{tabular}{>{\bfseries}lp{10cm}}
Temperature: & %(temperature)s \textcelsius \\
Atmospheric Pressure: & %(pressure)s hPa \\
Observer Height: & %(observer_height)s meters \\
\end{tabular}

\vspace{1cm}

\subsection*{Assumed Position}

\begin{tabular}{>{\bfseries}lp{10cm}}
Latitude: & %(assumed_lat)s \\
Longitude: & %(assumed_lon)s \\
\end{tabular}

\vspace{1cm}

\subsection*{Instrument Parameters}

\begin{tabular}{>{\bfseries}lp{10cm}}
Instrument Error: & %(instrument_error)s \\
Index Error: & %(index_error)s \\
Personal Error: & %(personal_error)s \\
\end{tabular}

\vspace{1cm}

\subsection*{Task}

Using the sight reduction method of your choice, calculate:
\begin{enumerate}
    \item The computed altitude ($H_c$) and azimuth ($Z_n$) for the assumed position
    \item The intercept ($a$) and its direction (Toward/Away from the celestial body)
    \item Plot the line of position on a plotting sheet
\end{enumerate}

\vspace{1cm}

\begin{tikzpicture}[scale=0.8]
  \draw[step=1cm,gray,very thin] (0,0) grid (12,8);
  \draw[thick] (0,0) rectangle (12,8);
  \node at (6,7.5) {\textbf{PLOTTING AREA}};
  \node at (6,7) {Use this space to plot your line of position};
\end{tikzpicture}

\vspace{1cm}

\subsection*{Solution Space}

\vspace{8cm} % Leave space for calculations

\newpage

% Plot Page
\section*{Sight Reduction Plot}

%(plot_include)s

\newpage

% Annexes with Almanac Data
\section*{Annexes}

%(almanac_annexes)s

%(additional_tables)s

\newpage

% Solution Page
\section*{Exercise Solutions}

%(solutions)s

\end{document}
"""

# Function to format data for LaTeX templates
def format_angle_for_latex(angle_degrees):
    """Format angle in degrees as D\textdegree M' S.S'' for LaTeX."""
    degrees = int(abs(angle_degrees))
    minutes_float = (abs(angle_degrees) - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    direction = "S" if angle_degrees < 0 else "N"
    if angle_degrees < 0:
        angle_degrees = -angle_degrees
    return f"{degrees}\\textdegree {minutes:02d}' {seconds:04.1f}''{direction}"

def format_lon_for_latex(lon_degrees):
    """Format longitude in degrees as D\textdegree M' S.S'' for LaTeX."""
    degrees = int(abs(lon_degrees))
    minutes_float = (abs(lon_degrees) - degrees) * 60
    minutes = int(minutes_float)
    seconds = (minutes_float - minutes) * 60
    direction = "W" if lon_degrees < 0 else "E"
    if lon_degrees < 0:
        lon_degrees = -lon_degrees
    return f"{degrees}\\textdegree {minutes:02d}' {seconds:04.1f}''{direction}"

def format_time_for_latex(datetime_obj):
    """Format datetime as YYYY-MM-DD HH:MM:SS for LaTeX."""
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S UTC")
