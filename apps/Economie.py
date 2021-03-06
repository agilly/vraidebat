import pandas as pd
from bokeh.plotting import figure, output_notebook, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool, BoxSelectTool, LassoSelectTool, PointDrawTool
from random import random

from bokeh.layouts import row, column
from bokeh.models import CustomJS, ColumnDataSource
from bokeh.plotting import figure, output_file, show
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn, NumberFormatter, HTMLTemplateFormatter, Panel, Tabs
from bokeh.io import output_file, show
from bokeh.layouts import widgetbox,layout
from bokeh.models.widgets import Slider, Div, Button, Toggle
from bokeh.models.glyphs import Text
from os.path import dirname,join
from bokeh.io import curdoc

base=["Economie"]
long=['Economie, Finances, Travail, Compte public']

for ix in range(0, len(base)):
    b=base[ix]
    ti=long[ix]
    i=b+".csv"
    o=b+".html"
    df = pd.read_csv(i)
    df['lcol']="#00000000"
    df.ptcex=df.ptcex*10
    df['id']=list(df.index)
    df['txt_alpha']=0
    df2=df.copy(deep=True)
    source=ColumnDataSource(df)
    s2 = ColumnDataSource(data=dict(id=[], n_vote=[], vote=[], title=[], body=[]))
    filsource=ColumnDataSource(df2)
    output_file(o)
    #wi=900
    div = Div(text="""Sélectionner des points pour afficher les satistiques.""")
#   div = Div(text="""Sélectionner des points pour afficher les satistiques.""", width=wi, height=50)

    p1 = figure(plot_height=600, title=ti, tools='box_select,lasso_select,box_zoom,wheel_zoom,reset', plot_width=900)
#    p1 = figure(plot_height=600, plot_width=wi, title=ti, tools='box_select,lasso_select,box_zoom,wheel_zoom')

    r1=p1.circle('tsneX', 'tsneY', source=filsource, alpha=0.6, size='ptcex', color='ptcol', line_color="lcol", line_width=3)
    txt=Text(x='tsneX', y='tsneY', text='title', text_alpha='txt_alpha', text_align='center')
    p1.add_glyph(filsource, txt)
    
    hover = HoverTool()
    hover.tooltips=[
        ('Votes', '@n_vote'),
        ('Adoption', '@vote'),
        ('Titre', '@title')]
    hover.renderers=[r1]

    p1.add_tools(hover)
    tool = PointDrawTool(renderers=[r1], num_objects=2000)
    p1.add_tools(tool)

    filsource.selected.js_on_change('indices', CustomJS(args=dict(source=filsource, s2=s2, div=div), code="""
            var inds = cb_obj.indices;
            var d1 = source.data;
            var d2 = s2.data;
            d2['vote'] = []
            d2['n_vote'] = []
            d2['title'] = []
            d2['body'] = []
            d2['id'] = []
            var totvot=0;
            var tota=0
            for (var i = 0; i < inds.length; i++) {
                d2['vote'].push(d1['vote'][inds[i]])
                d2['n_vote'].push(d1['n_vote'][inds[i]])
                d2['title'].push(d1['title'][inds[i]])
                d2['body'].push(d1['body'][inds[i]])
                d2['id'].push(d1['id'][inds[i]])
                totvot=totvot+d1['n_vote'][inds[i]]
                tota=tota+d1['n_vote'][inds[i]]*d1['vote'][inds[i]]
            }
            tota=tota/totvot;
            s2.change.emit();
            div.text="<b>Total votes: </b> "+totvot;
            div.text=div.text+"<br><b>Approbation: </b>";
            div.text=div.text+tota;
        """)
    )

    s2.selected.js_on_change('indices', CustomJS(args=dict(source=filsource, s2=s2, div=div), code="""
            var inds = cb_obj.indices;
            var d1 = source.data;
            var d2 = s2.data;
            toselect = []
            var totvot=0
            var tota=0
            for (var i = 0; i < inds.length; i++) {
                toselect.push(d2['id'][inds[i]])
                totvot=totvot+d2['n_vote'][inds[i]]
                tota=tota+d2['n_vote'][inds[i]]*d2['vote'][inds[i]]
            }

            //alert(toselect)
            for (var i = 0; i < d1['id'].length; i++) {
                for(var j = 0; j < toselect.length; j++){
                if(d1['id'][i]==toselect[j])
                {
                    d1['lcol'][i]="#b22222ff"
                    break;
                }else{
                    d1['lcol'][i]="#00000000"
                }

                }
            }
            source.change.emit();
            tota=tota/totvot;
            div.text="<b>Total votes: </b> "+totvot;
            div.text=div.text+"<br><b>Approbation: </b>";
            div.text=div.text+tota;
            div.text=div.text+"<br><b>Sélection:</b>";
            div.text=div.text+toselect
        """)
    )

    filtervote=CustomJS(args=dict(source=source, filsource=filsource, s2=s2, div=div), code="""
            var cutoff_n = nvote.value;
            var cutoff = vote.value;
            var showtxt = txt.active;
            cutoff=cutoff/100;
            var mastersrc= source.data;
            var plotsrc = filsource.data;
            //var tablesrc = s2.data;
            plotsrc['vote'] = []
            plotsrc['n_vote'] = []
            plotsrc['title'] = []
            plotsrc['body'] = []
            plotsrc['id'] = []
            plotsrc['tsneX'] = []
            plotsrc['tsneY'] = []
            plotsrc['ptcol'] = []
            plotsrc['ptcex'] = []
            plotsrc['txt_alpha'] = []
            //alert(!ci.active)
            thr=0.05/(mastersrc['p_prop'].length)
            for (var i = 0; i < mastersrc['vote'].length; i++) {
                if(((mastersrc['n_vote'][i])>cutoff_n)  && ( ((mastersrc['vote'][i])>cutoff) || ((mastersrc['vote'][i])<(1-cutoff)) )){
                    if((!ci.active) || (mastersrc['p_prop'][i]<thr)){
                    plotsrc['vote'].push(mastersrc['vote'][i])
                    plotsrc['n_vote'].push(mastersrc['n_vote'][i])
                    plotsrc['title'].push(mastersrc['title'][i])
                    plotsrc['body'].push(mastersrc['body'][i])
                    plotsrc['id'].push(mastersrc['id'][i])
                    plotsrc['tsneX'].push(mastersrc['tsneX'][i])
                    plotsrc['tsneY'].push(mastersrc['tsneY'][i])
                    plotsrc['ptcol'].push(mastersrc['ptcol'][i])
                    plotsrc['ptcex'].push(mastersrc['ptcex'][i])
                    if(showtxt){
                        plotsrc['txt_alpha'].push(1)
                    }else{
                        plotsrc['txt_alpha'].push(0)
                    }
                    
                    }
                }
            }
            filsource.change.emit();
        """)
    

    
    columns = [
            TableColumn(field="n_vote", title="Votes", width=20),
            TableColumn(field="vote", title="Approbation", width=20, formatter=NumberFormatter(format='0.00')),
            TableColumn(field="title", title="Titre", formatter=HTMLTemplateFormatter(template='<div><%= title %></div>')),
            TableColumn(field="body", title="Corps", formatter=HTMLTemplateFormatter(template='<div><%= body %></div>')),
        ]

    p2= DataTable(source=s2, columns=columns, width=1200)
#    p2= DataTable(source=s2, columns=columns, width=wi, height=400)


    end_slider=max(df.n_vote)
    nvote_slider = Slider(start=0, end=end_slider, value=0,step=10, title="Nombre de votes minimum", callback=filtervote)
    filtervote.args["nvote"] = nvote_slider
    vote_slider = Slider(start=50, end=100, value=50, title="Approbation/rejet(%)", callback=filtervote)
    filtervote.args["vote"] = vote_slider
    
    toggle = Toggle(label="Cacher points non significatifs", callback=filtervote, width=50)
    toggle_expl=Div(text="""Ce bouton masque les propositions dont l'approbation <b>ne peut pas être distinguée statistiquement de 50%</b>. Par exemple, une approbation de 60% ne veut presque rien dire si on la calcule sur 10 votes, par contre sur 5000 on est sûr qu'une majorité des votants est d'accord avec la proposition.Formellement, ce filtrage est obtenu par un test binomial exact bi-directionnel avec correction de Bonferroni.""")
    toggletxt = Toggle(label="Afficher le titre des revendications", callback=filtervote, width=50)
    toggletxt_exp = Div(text="""<b>Attention:</b> Filtrer les points et/ou zoomer avant d'afficher le texte pour que le graphique reste lisible.""")
    filtervote.args["ci"]=toggle
    filtervote.args["txt"]=toggletxt

    dl = Button(label="Télécharger données filtrées", button_type="success")
    dl.callback = CustomJS(args=dict(source=filsource),
                           code=open(join(dirname(__file__), "download.js")).read())

    
    bbox=column([nvote_slider, vote_slider, toggle, toggle_expl, toggletxt, toggletxt_exp, dl])
    
#    l=layout([[p1, bbox]], sizing_mode='stretch_both') # sizing mode is completely broken, fixed widths it is :(
    l=layout([[p1, bbox], [div], [p2]])
    #layout = column(sli1,p1)
    l.sizing_mode = 'scale_width'
    
    #show(l)
    curdoc().add_root(l)
