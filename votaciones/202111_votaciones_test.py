from votaciones.servelscraper import list_elections
from votaciones.servelscraper import ServelScraper
from selenium import webdriver
from pathlib import Path

tempdir = r'G:\Proyectos\elecciones\202111\raw_data'
chromedriver = r'G:\Proyectos\elecciones\chromedriver.exe'
logPath = Path(r'G:\GIT\servel\servel_scraper\votaciones')

options = webdriver.ChromeOptions()
# options.add_argument("--headless")
options.add_argument("--log-level=3")
options.add_experimental_option("prefs", {
    "download.default_directory": format(tempdir),
    "download.prompt_for_download": False,
})

url_base = 'servelelecciones.cl'

list_elections(chromedriver, url_base)

driver = webdriver.Chrome(executable_path=chromedriver, options=options)
driver.implicitly_wait(3)

scrap = ServelScraper(driver=driver,
                      log_path=logPath,
                      mainurl=url_base,
                      name='participacion_2021_pv',
                      election='participacion',
                      debug=False)
scrap.get_elections_list()

# Para optimizar, es necesario obtener un listado de las circunscripciones antes de repartir el trabajo
# Usualmente es cirunscripción electoral, que el nivel superior antes de que se deba hacer una elección en el siguiente nivel
# y abrir los resultados: se puede ver en config.DIV_FILTERS
scrap.get_levels('circ_electoral', overwrite=False)



scrap = ServelScraper(driver=driver,
                      log_path=logPath,
                      mainurl=url_base,
                      name='participacion_2021_pv',
                      election='participacion',
                      debug=False,
                      output_folder='out')
scrap.set_driver(driver)
scrap.get_levels('circ_electoral', overwrite=False)

sl = scrap.levels.iloc[0]

ans = scrap.export_unfold(start='locales',
                   val=sl.cod_circ,
                   REG={'regiones': {'c': sl.cod_reg, 'd': sl.reg},
                        'circ_senatorial': {'c': sl.cod_cs, 'd': sl.cs},
                        'distritos': {'c': sl.cod_dis, 'd': sl.dis},
                        'comunas': {'c': sl.cod_com, 'd': sl.com},
                        'circ_electoral': {'c': sl.cod_circ, 'd': sl['circ']}
                        },
                   stop_on=None,
                   stop_proc='locales',
                   data_list=[])
