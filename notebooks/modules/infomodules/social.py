#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: lmh
"""
import matplotlib.pyplot as plt
import networkx as nx
import networkx.algorithms.community as nxcom
import pandas as pd
import numpy as np
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

        self.version = "0.1.0"
        
        self.tmpdir = os.getcwd()
        
        self.names = None
        
        self.G = None
        self.fig = None
        self.cons = None
        self.clique = None
        self.communities = None
        self.centrality = None
        
        self.template = ""
        self.set_template()
        
        self.rendervars = {'cons':'', 'cliques':'', 'nocliq':'', 'comms':'', 'version':self.version }

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

    def get_closeness_centrality(self,nodes):
        centrality = nx.closeness_centrality(self.G.subgraph(nodes))
        W=np.array([k for v,k in centrality.items()]).sum()
        return { k:v/W for k,v in centrality.items() }
    
    def get_communities(self):
        self.communities = sorted(nxcom.greedy_modularity_communities(self.G), key=len, reverse=True)

        comms = { k+1:list(v) for k,v in enumerate(self.communities) }
        columns = [ j+1 for j in range(np.array([ len(v) for k,v in comms.items() ]).max()) ]
        DF_c = pd.DataFrame.from_dict(comms,orient='index',columns=columns).T
        DF_c_a = { k:DF_c[[k]] for k in DF_c.keys() }

        def get_c_c(name,centrality):
            if isinstance(name,type(None)):
                return None
            else:
                return centrality[name] * 100
            
        def get_b_c(name):
            if isinstance(name,type(None)):
                return None
            else:
                return self.centrality[name] * 100

        def reformat_name(df):
            if not pd.isna(df['c']):
                key_c = list(set(df.keys())-set(['c','b']))[0]
                return "{name} ({c:.1f}%)".format(name=df[key_c],c=df['c'])
            else:
                return None

        for c in DF_c_a.keys():
            DF_tmp = DF_c_a[c].copy()
            centrality = self.get_closeness_centrality(DF_tmp[c].values)
            DF_tmp['c'] = DF_tmp[c].apply(lambda k: get_c_c(k,centrality))
            DF_tmp['b'] = DF_tmp[c].apply(get_b_c)
            DF_tmp = DF_tmp.sort_values('c',ascending=False).reset_index(drop=True)
            DF_tmp[c] = DF_tmp.apply(reformat_name,axis=1)
            DF_tmp.loc[len(DF_tmp.index)] = ["{c:.1f}%".format(c=DF_tmp['b'].sum()), None, None] 
            DF_c_a[c] = DF_tmp[[c]]
            
        DF_c_a = pd.concat(DF_c_a.values(),axis=1)
        DF_c_a.fillna('', inplace=True)

        self.rendervars['comms'] = DF_c_a.to_latex(index=False)
        
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

    def get_centrality(self):
        centrality = nx.betweenness_centrality(self.G, normalized=True, endpoints=False)
        W=np.array([k for v,k in centrality.items()]).sum()
        self.centrality = {k:v/W for k,v in centrality.items() }
        
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
            
        

        self.fig, ax = plt.subplots(1,1,figsize=(11.69*2,8.27*2))

        if not directed:
            self.get_centrality()
            cons  = pd.DataFrame.from_dict({'name': list(self.centrality.keys()), 'vernetzung': list(self.centrality.values())})
            cons = cons.sort_values(['vernetzung'],ascending=False).reset_index(drop=True)
            cons['vernetzung'] = cons['vernetzung'].apply(lambda x: "{:.1f}%".format(x*100))
            cons.rename(columns={'vernetzung':'Zentralität', 'name':'Name'}, inplace=True)
            self.cons = cons
            self.rendervars['cons'] = self.cons.to_latex(index=False)

            self.get_communities()
            self.set_node_community(self.G, self.communities)
            self.set_edge_community(self.G)
            node_color = [self.get_color(self.G.nodes[v]['community']) for v in self.G.nodes]
            node_size = [ (1+self.centrality[k])**10*500 for k in self.G.nodes ]
            external = [(v, w) for v, w in self.G.edges if self.G.edges[v, w]['community'] == 0]
            internal = [(v, w) for v, w in self.G.edges if self.G.edges[v, w]['community'] > 0]
            internal_color = ['black' for e in internal]

            pos = nx.spring_layout(self.G)
            plt.box(False)

            nx.draw_networkx(
                    self.G,
                    ax=ax,
                    pos=pos,
                    alpha=1,
                    width=1,
                    node_size=0,
                    edgelist=external,
                    edge_color="silver",
                    )
            nx.draw_networkx(
                    self.G,
                    ax=ax,
                    pos=pos,
                    alpha=1,
                    width=1,
                    node_color=node_color,
                    node_size=node_size,
                    edgelist=internal,
                    edge_color=internal_color,
                    )

        else:
            pos = nx.spring_layout(self.G)
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

    def set_node_community(self, G, communities):
        '''
        Add community to node attributes
        https://graphsandnetworks.com/community-detection-using-networkx/
        '''
        for c, v_c in enumerate(communities):
            for v in v_c:
                # Add 1 to save 0 for external edges
                G.nodes[v]['community'] = c + 1

    def set_edge_community(self, G):
        '''
        Find internal edges and add their community to their attributes.
        https://graphsandnetworks.com/community-detection-using-networkx/
        '''
        for v, w, in G.edges:
            if G.nodes[v]['community'] == G.nodes[w]['community']:
                # Internal edge, mark with community
                G.edges[v, w]['community'] = G.nodes[v]['community']
            else:
                # External edge, mark as 0
                G.edges[v, w]['community'] = 0

    def get_color(self, i, r_off=1, g_off=1, b_off=1):
        '''
        Assign a color to a vertex.
        https://graphsandnetworks.com/community-detection-using-networkx/
        '''
        r0, g0, b0 = 0, 0, 0
        n = 16
        low, high = 0.1, 0.9
        span = high - low
        r = low + span * (((i + r_off) * 3) % n) / (n - 1)
        g = low + span * (((i + g_off) * 5) % n) / (n - 1)
        b = low + span * (((i + b_off) * 7) % n) / (n - 1)
        return (r, g, b)

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
        self.get_communities()
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
\usepackage{xcolor}
\usepackage{multicol}
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
\usepackage{courier}
\fancypagestyle{pdfreport}{%
\fancyheadoffset{0.25cm} 
\fancyhf{}
\fancyhead[LE,RO]{\today}
\fancyhead[RE,LO]{Soziogramm Report}
\fancyhead[CO,CE]{}
\fancyfoot[CE,CO]{\leftmark}
\fancyfoot[CE,CO]{Seite \thepage}
\fancyfoot[R]{v{% endraw %}{{ version }}{% raw %}}
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

\begin{minipage}[t]{0.6\textwidth}
\vspace{-0.2cm}
\href{https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.clique.find_cliques.html#networkx.algorithms.clique.find_cliques}{\textbf{Cliquen:}}
\vspace{-0.2cm}
\begin{multicols}{3}
\begin{itemize}
\setlength\itemsep{0pt}
{% endraw %}{{ cliquen }}{% raw %}
\end{itemize}
\end{multicols}
{\color{red} \bf
{% endraw %}
{% if nocliq!='' %}
Nicht in Cliquen: {{nocliq}}
{% endif %}
{% raw %}
}
\vspace{0.5cm}
\href{https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.community.modularity_max.greedy_modularity_communities.html#networkx.algorithms.community.modularity_max.greedy_modularity_communities}{\textbf{Communities:}}\par
Gruppierungen in der Klasse mit \href{https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.closeness_centrality.html}{\texttt{closeness}-Zentralität und Zentralität}.\par
\vspace{0.2cm}
{% endraw %}{{ comms }}{% raw %}
\vspace{0.4cm}
Hinter jedem Namen ist die (auf die Gruppe normierte) \texttt{closeness}-Zentralität angegben. Dies gibt den Einfluss der Person auf die Gruppe an. Unter der Gruppe
ist jeweis die Summe der Zentralitäten angegeben - so viel Einfluss hat die Gruppe auf die gesamte Klasse.
\end{minipage}
\hfill
\begin{minipage}[t]{0.3\textwidth}
\vspace{0pt}
{% endraw %}{{ cons }}{% raw %}
\vspace{0.1cm}
Die Zentralität (Graphentheorie) gibt an, wie viel Einfluss ein Knotenpunkt auf ein Netzwerk hat.
(\href{https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.centrality.betweenness_centrality.html}{hier}: \texttt{betweenness\_centrality(G, k=None, normalized=True, weight=None, endpoints=False})\par
Die Zentralität einer Klasse ist auf die Summe 100\% normiert.
\end{minipage}
\par
\begin{minipage}[t]{\textwidth}
Bild 1: Gegenseitige Verbindungen mit Communities\par
\includegraphics[width=0.9\textwidth]{soziogramm1.pdf}\\
\end{minipage}
\par
\begin{minipage}[t]{\textwidth}
Bild 2: Alle Verbindungen \par
\includegraphics[width=0.9\textwidth]{soziogramm2.pdf}\\
\end{minipage}
\par

\end{document}
{% endraw %}
"""