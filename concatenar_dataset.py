import pandas as pd

pagina_siete = pd.read_csv('paginasiete.csv')
la_razon = pd.read_csv('larazon.csv')
el_deber = pd.read_csv('eldeber.csv')
la_prensa = pd.read_csv('laprensa.csv')

df = pd.concat([la_razon,el_deber,la_prensa,pagina_siete], axis = 0)
df.to_csv('noticias.csv', index = False)