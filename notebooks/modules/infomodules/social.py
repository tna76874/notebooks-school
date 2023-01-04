#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lmh
"""
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nxcom
import pandas as pd
import os
from itertools import combinations,chain
from jinja2 import Environment, BaseLoader
import shutil

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


class soziogramm(object):
    def __init__(self,**kwargs):
        self.config = {}
        self.config.update(kwargs)
        
        self.tmpdir = os.getcwd()
        
        self.names = None
        
        self.G = None
        self.fig = None
        self.cons = None
        self.clique = None
        
        self.template = ""
        self.set_template()
        
        self.rendervars = {'cons':'', 'cliques':'', 'nocliq':'', 'comms':''}

    def read_names(self):
        self.names = pd.read_csv('namen.csv', header=None)
    
    def save(self, format='pdf', name='soziogramm'):
        self.fig.savefig(os.path.join(self.tmpdir,name+"."+format))
    
    def rendertex(self):
        renderfile = os.path.join(self.tmpdir,'report.tex')
        
        template = Environment(loader=BaseLoader).from_string(self.template)
        template_out = template.render(**self.rendervars)

        with open(renderfile, "w",encoding="utf8") as myfile:
            myfile.write(template_out) 
        
    def get_clique(self):
        self.clique = [ list(k) for k in nx.find_cliques(self.G) if len(k)>2 ]
        in_clique = list()
        for i in self.clique: in_clique+=i
        in_clique = list(set(in_clique))
        not_in_clique = [ k for k in self.G.nodes() if (k not in in_clique) ]
        
        cliques = [ ", ".join(k) for k in self.clique ]
        cliques_len = str(len(self.clique))
        
        self.rendervars['cliquen'] =  "\\item " + "\n\\item ".join(cliques)
        
        self.rendervars['nocliq'] = ", ".join(not_in_clique)

        communities = sorted(nxcom.greedy_modularity_communities(self.G), key=len, reverse=True)
        self.rendervars['comms'] = "\\item " + "\n\\item ".join([", ".join(k) for k in communities])
        
    def make_soziogramm(self, save=False, format='pdf', directed=False):
        self.read_names()
        
        pairs = list()
        personen = list()
        for i in self.names.index:
            n = [k for k in self.names.loc[i,:].values if pd.notnull(k)]
            personen += n
            pairs += [tuple([k,n[0]]) for k in n[1:]]
        weights = [ tuple(sorted(list(k))) for k in pairs]
        weights = {x:weights.count(x) for x in weights}
        personen = list(set(personen))
        print("In der Klasse sind {:} Personen.".format(len(personen)))

        if directed:
            self.G = nx.DiGraph()
        else:
            self.G = nx.Graph()
        
        self.G.add_nodes_from(personen)
        edgelist = list()
        edge_color = list()
        edge_style = list()
        for k in pairs:
            edgeweight=weights[tuple(sorted(list(k)))]
            if (edgeweight>=2) & directed:
                edge_color+=['r']
                edge_style+=['-']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            if (edgeweight>=2) & (not directed):
                edge_color+=['k']
                edge_style+=['-']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            elif (edgeweight<2) & directed:
                edge_color+=['k']
                edge_style+=[':']
                edgelist += [tuple(k)]
                self.G.add_edge(k[0], k[1], weight=edgeweight)
            
        pos = nx.spring_layout(self.G)

        self.fig, ax = plt.subplots(1,1,figsize=(11.69*2,8.27*2))
        nx.draw_networkx(self.G, pos,
                         with_labels=True,
                         ax=ax,
                         font_color='red',
                         node_size=1000,
                         node_color="white",
                         node_shape="s",
                         alpha=1,
                         width=1,
                         edgelist=edgelist,
                         style=edge_style,
                         edge_color=edge_color,
                        )
        
        
        ax.set_aspect('equal')
        plt.box(False)

        if save: self.save(format=format)

        if not directed:
            betCent = nx.betweenness_centrality(self.G, normalized=True, endpoints=True)
            cons  = pd.DataFrame.from_dict({'name': list(betCent.keys()), 'vernetzung': list(betCent.values())})
            cons = cons.sort_values(['vernetzung'],ascending=False).reset_index(drop=True)
            cons['vernetzung'] = cons['vernetzung'].apply(lambda x: "{:.0f}%".format(x*100))
            cons.rename(columns={'vernetzung':'Vernetzung', 'name':'Name'}, inplace=True)
            self.cons = cons
            self.rendervars['cons'] = self.cons.to_latex(index=False)

    def run_latex(self,input_filename, output_filename,runinfo=None,latex="/usr/bin/pdflatex",ending='tex'):
        input_filename = os.path.abspath(input_filename+'.'+ending)
        input_filename = (os.path.dirname(input_filename),os.path.basename(input_filename))

        output_filename = os.path.abspath(output_filename)
        output_filename = (os.path.dirname(output_filename),os.path.basename(output_filename))
        
        if not isinstance(runinfo,type(None)):
            print("Compiling {out}.pdf (Run {run}/{total})".format(out=output_filename[1],run=runinfo[0],total=runinfo[1]))
            
        cmd = [
            latex,
            '-output-format=pdf',
            '-jobname=' + output_filename[1],
            ]
        cmd += [
            input_filename[1],
            '>/dev/null 2>&1',
            ]
        os.system(" ".join(cmd))
        
    def create_pdf(self,input_filename, output_filename,n=2):
        self.run_latex(input_filename, output_filename)
        for i in range(n):
            self.run_latex(input_filename, output_filename,runinfo=(i+1,n))

    def ensure_dir(self,DIR):
        dirlist = os.path.normpath(DIR).split(os.sep)
        for i in range(len(dirlist)):
            tmpdir = os.path.abspath(os.sep.join(dirlist[:i+1]))
            if not os.path.exists(tmpdir):
                os.mkdir(tmpdir)
                
    def gen_report(self):
        self.tmpdir = "/tmp/report"
        self.ensure_dir(self.tmpdir)
        self.make_soziogramm()
        self.get_clique()
        self.save(name='soziogramm1')
        self.make_soziogramm(directed=True)
        self.save(name='soziogramm2')
        self.rendertex()
        rootdir = os.getcwd()
        os.chdir(self.tmpdir)
        pdfname = 'report'
        self.create_pdf('report',pdfname)
        shutil.copy(os.path.join(self.tmpdir,pdfname+'.pdf'),os.path.join(rootdir,pdfname+'.pdf'))
        os.chdir(rootdir)

            
    def set_template(self):
        self.template=r"""
{% raw %}\documentclass[a4paper]{article}
\usepackage[utf8]{inputenc}
\usepackage[ddmmyyyy]{datetime}
\renewcommand{\dateseparator}{.}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage[landscape]{geometry}
\usepackage[hidelinks]{hyperref}
\usepackage{hyperxmp}
\hypersetup{pdfauthor={Lukas Meyer-Hilberg}, 
	pdftitle={Soziogramm Report}, 
	pdfsubject={Soziogramm Report}, 
	pdfcreator={LaTeX}, 
	pdfproducer={LaTeX}, 
	pdfkeywords={Stand \today}, 
	pdfcopyright={Lukas Meyer-Hilberg}}
\usepackage{fancyhdr}
\pagestyle{fancy}
\fancypagestyle{pdfreport}{%
\fancyheadoffset{0.25cm} 
\fancyhf{}
\fancyhead[LE,RO]{\today}
\fancyhead[RE,LO]{Soziogramm Report}
\fancyhead[CO,CE]{}
\fancyfoot[CE,CO]{\leftmark}
\fancyfoot[CE,CO]{Seite \thepage}
\fancyfoot[R]{}
\fancyfoot[L]{\textcopyright\,Hilberg\,\the\year{}}
}
\pagestyle{pdfreport}
\geometry{
a4paper,
left=10mm,
right=10mm,
top=20mm,
bottom=20mm,
}
% Helvetica font
\usepackage{helvet}
\renewcommand{\familydefault}{\sfdefault}
%
\setlength\parindent{0pt}

\begin{document}

\begin{minipage}[t]{0.5\textwidth}
\vspace{-0.2cm}
Cliquen:
\vspace{-0.2cm}
\begin{itemize}
\setlength\itemsep{0pt}
{% endraw %}{{ cliquen }}{% raw %}
\end{itemize}
{% endraw %}
{% if nocliq!='' %}
Nicht in Cliquen: {{nocliq}}
{% endif %}
{% raw %}
\href{https://networkx.org/documentation/stable/reference/algorithms/community.html#module-networkx.algorithms.community}{Communities}
\vspace{-0.2cm}
\begin{itemize}
\setlength\itemsep{0pt}
{% endraw %}{{ comms }}{% raw %}
\end{itemize}
\end{minipage}
\begin{minipage}[t]{0.5\textwidth}
\vspace{0pt}
\href{https://en.wikipedia.org/wiki/Betweenness_centrality}{Vernetzung: Betweenness centrality}\par
{% endraw %}{{ cons }}{% raw %}
\end{minipage}

\begin{minipage}[t]{\textwidth}
\vspace{0.5cm}
Bild 1: Gegenseitige Verbindungen \par
\includegraphics[width=\linewidth]{soziogramm1.pdf}\\
\end{minipage}
\par
\begin{minipage}[t]{\textwidth}
\vspace{0.5cm}
Bild 2: Alle Verbindungen \par
\includegraphics[width=\linewidth]{soziogramm2.pdf}\\
\end{minipage}
\par

\end{document}
{% endraw %}
"""