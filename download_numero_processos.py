import requests as req
import logging
import os
from datetime import datetime
from bs4 import BeautifulSoup
from settings import Settings
import threading
from downloadsentences import DownloadSetence
import platform
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class Extract_Numbers:

    def __init__(self, id, pagInit, pagEnd, driver, num = 0):
        self.arquivo = None
        self.s = Settings()
        self.s.extract_settings()
        self.create_log_(id)
        self.id = id
        self.pagInit = 1 if pagInit == 0 else pagInit
        self.pagEnd = pagEnd
        self.num = num
        self.arquivos = []
        self.driver = driver


    def create_log_(self, id):
        name = "log_extract_numbers_" + str(id)
        self.log_file = "log_extract_numbers_" + str(id) + "_" + datetime.now().strftime("%d%m%Y_%H_%M")
        self.logger = self.s.createLogFile(name, self.log_file)

    def extrai_numero_processo(self, id, response):
        page = BeautifulSoup(response.content, "html.parser")
        div = page.find("div", {"id": "divDadosResultado"})
        if div is None:
            self.logger.debug("Nao encontrou a div de dados")
            return 0

        as_tag = div.find_all("a")
        if as_tag is None:
            return None
        names = set()
        for a in as_tag:
            names.add(a["name"])
        self.save_processos(id, names)

    def save_processos(self, id, names):
        if self.num + len(names) < 10000 and self.arquivo is not None:
            arquivo = self.arquivo 
        else:
            arquivo = "resultado_" + str(id) + "_" + datetime.now().strftime("%d%m%Y_%H_%M") + ".txt"
            print(arquivo)
            self.arquivo = arquivo
            self.arquivos.append(self.arquivo)
            self.num = 0
        
        with open(os.path.join(self.s.path, "numero_processos", arquivo), "a") as f:
            for n in names:
                f.write(n)
                f.write("\n")
        self.num += len(names)

    def download(self):
        start = datetime.now()
        session = req.Session()
        response = session.get("http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=8816%2C8817%2C8592%2C8593%2C4052%2C4062%2C8587%2C8588%2C8589%2C8590%2C8714%2C8501%2C8791%2C8792%2C8505%2C8507%2C8508%2C8509%2C8510%2C8512%2C8513%2C8514%2C8515%2C8518%2C8519%2C8520%2C8521%2C4060%2C2061%2C8724%2C8738%2C8523%2C8524%2C8525%2C8526%2C8527%2C8529%2C8530%2C8531%2C8532%2C8533%2C8780%2C8781%2C8819%2C8822%2C4294%2C4295%2C8548%2C8549%2C8550%2C8551%2C8552%2C8553%2C8554%2C8555%2C8556%2C8557%2C8559%2C8560%2C8561%2C8562%2C8563%2C8564%2C8565%2C8566%2C8567%2C8568%2C8569%2C8570%2C8571%2C8572%2C8573%2C8574%2C8575%2C8576%2C8577%2C8578%2C8579%2C8580%2C8581%2C8582%2C8583%2C8584%2C8585%2C8535%2C8536%2C8537%2C8538%2C8539%2C8540%2C8541%2C8544%2C8546%2C2019%2C2070%2C2071%2C2072%2C2075%2C2079%2C2080%2C2081%2C988%2C8723%2C8602%2C8595%2C4053%2C8597%2C8598%2C8719%2C8721%2C8722%2C8614%2C8616%2C8618%2C8619%2C8620%2C4824%2C8547%2C8798%2C8799%2C2100%2C2104%2C2023%2C2024%2C2105%2C2106%2C2107%2C2111%2C2027%2C8782%2C8624%2C8627%2C8728%2C8729%2C8629%2C8632%2C8634%2C8635%2C4049%2C4054%2C4055%2C2029%2C4278%2C2052%2C2026%2C4056%2C8785%2C8637%2C8638%2C8639%2C8640%2C4296%2C9640%2C2020%2C2900%2C4290%2C4291%2C4292%2C8800%2C2048%2C2050%2C2201%2C2206%2C2207%2C2209%2C2211%2C2212%2C8712%2C8713%2C8825%2C8823%2C8704%2C8733%2C8734%2C8735%2C8706%2C8707%2C8708%2C8709%2C8710%2C4825%2C4284%2C4285%2C4286%2C4287%2C4288%2C4289%2C8794%2C8820%2C8827%2C8828%2C8829%2C8737%2C8797%2C8698%2C8699%2C4051%2C2187%2C2189%2C2190%2C2053%2C8692%2C8693%2C8695%2C8696%2C8685%2C8686%2C8687%2C8688%2C8689%2C8690%2C8691%2C8795%2C8796%2C8656%2C8657%2C8803%2C8804%2C8649%2C8650%2C2155%2C4282%2C8652%2C8653%2C8654%2C8647%2C8801%2C8832%2C8660%2C8661%2C8662%2C8663%2C8793%2C8665%2C8666%2C8667%2C8668%2C8669%2C8670%2C4283%2C8673%2C8674%2C8675%2C8677%2C8678%2C8679%2C8681%2C8682%2C8806%2C8732%2C9903%2C8830%2C2901%2C2902%2C2903%2C8765%2C8766%2C8812%2C8813%2C8814%2C8809%2C8810%2C8811%2C8802%2C8745%2C8746%2C8747%2C8748%2C8749%2C8750%2C8751%2C8752%2C8753%2C8754%2C8755%2C8756%2C8757%2C8758%2C8759%2C8783%2C8784%2C8787%2C8788%2C8789%2C8790%2C4050%2C4044%2C8761%2C8762%2C8763%2C8818%2C4281%2C4046%2C4047%2C4048%2C8772%2C8773%2C8774%2C8775%2C8776%2C8805%2C8815%2C8831%2C8727%2C8731%2C8740%2C8741%2C8742%2C9638%2C9639%2C4064%2C2002%2C2003%2C2004%2C2006%2C2008%2C2011%2C2013%2C2014%2C4293%2C8833%2C9655%2C9656%2C7%2C9997%2C9675%2C9650%2C9651%2C9652%2C9653%2C9654%2C9658%2C9659%2C9011%2C9012%2C9013%2C9019%2C9021%2C9041%2C9047%2C9048%2C9049%2C9053%2C9054%2C9055%2C9056%2C9072%2C9076%2C9086%2C9087%2C9094%2C9095%2C9096%2C9097%2C9099%2C9103%2C9106%2C9110%2C9111%2C9135%2C9136%2C9137%2C9140%2C9142%2C9143%2C9145%2C9158%2C9159%2C9160%2C9161%2C9164%2C9172%2C9176%2C9180%2C9181%2C9184%2C9186%2C9367%2C9368%2C9369%2C9370%2C9371%2C9372%2C9373%2C9374%2C9375%2C9377%2C9378%2C9379%2C9380%2C9381%2C9382%2C9383%2C9384%2C9385%2C9386%2C9387%2C9388%2C9389%2C9392%2C9441%2C9453%2C9663%2C9665%2C9667%2C9669%2C9671%2C9673%2C9679%2C9681%2C9683%2C9687%2C9696%2C9821%2C9823%2C9825%2C9827%2C9829%2C9831%2C9833%2C9641%2C9643%2C9645%2C9647%2C9649%2C9657%2C9660%2C8834%2C8836%2C8838%2C8840%2C8842%2C8844%2C8846%2C8848%2C8850%2C8852%2C8854%2C8856%2C8858%2C8860%2C8862%2C8864%2C8866%2C8868%2C8870%2C8872%2C8874%2C8876%2C8878%2C8880%2C8882%2C8884%2C8886%2C8888%2C8890%2C8892%2C8894%2C8896%2C8898%2C8900%2C8902%2C8918%2C8924%2C8926%2C8940%2C8946%2C8950%2C8952%2C8954%2C8956%2C8958%2C8960%2C8962%2C8964%2C8970%2C8972%2C8974%2C8976%2C8978%2C9064%2C9155%2C9162%2C9165%2C9169%2C9173%2C9175%2C9178%2C9269%2C9279%2C9390%2C9398%2C9402%2C9405%2C9431%2C9433%2C9435%2C9439%2C9443%2C9458%2C9460%2C9466%2C9470%2C9488%2C9492%2C9494%2C9496%2C9498%2C9601%2C9603%2C9605%2C9607%2C9609%2C9637%2C8001%2C8002%2C8003%2C8004%2C8005%2C8006%2C8007%2C8008%2C8009%2C8010%2C8011%2C8012%2C8013%2C8014%2C8015%2C8017%2C8018%2C8019%2C8020%2C8021%2C8022%2C8023%2C8024%2C8025%2C8026%2C8027%2C8028%2C8029%2C8030%2C8031%2C8032%2C8033%2C8034%2C8036%2C8038%2C8039%2C8040%2C8041%2C8042%2C8043%2C8044%2C8045%2C8046%2C8047%2C8048%2C8049%2C8050%2C8051%2C8052%2C8054%2C8055%2C8056%2C8057%2C8058%2C8059%2C8060%2C8061%2C8062%2C8064%2C8065%2C8066%2C8067%2C8068%2C8069%2C8070%2C8072%2C8073%2C8074%2C8075%2C8076%2C8077%2C8078%2C8079%2C8081%2C8083%2C8121%2C8212%2C8224%2C8226%2C8228%2C8230%2C8232%2C8234%2C8236%2C8238%2C8240%2C8242%2C8244%2C8248%2C8250%2C8258%2C8260%2C8262%2C8264%2C8266%2C8268%2C8270%2C8272%2C8274%2C8276%2C8278%2C8280%2C8282%2C8284%2C8286%2C8288%2C8290%2C8292%2C8294%2C8296%2C8300%2C8302%2C8304%2C8306%2C8308%2C8310%2C8312%2C8314%2C8316%2C8318%2C8320%2C8322%2C8324%2C8326%2C8328%2C8330%2C8332%2C8356%2C8358%2C8362%2C8364%2C8386%2C8392%2C8394%2C8396%2C8400%2C8406%2C8414%2C8416%2C8428%2C8432%2C8434%2C8436%2C8438%2C8442%2C8444%2C8446%2C8448%2C8450%2C8452%2C8456%2C8458%2C8460%2C8462%2C8464%2C8466%2C8468%2C8470%2C8472%2C8474%2C8476%2C8478%2C8480%2C8482%2C8484%2C8488%2C8490%2C8492%2C8494%2C8496%2C8498%2C9962%2C9964%2C9966%2C9968%2C9970%2C9984%2C9986%2C9988%2C9990%2C9992%2C9994%2C11%2C284%2C325%2C398%2C400%2C402%2C406%2C415%2C424%2C430%2C432%2C435%2C438%2C442%2C448%2C454%2C456%2C459%2C462%2C464%2C466%2C468%2C470%2C472%2C474%2C476%2C478%2C480%2C482%2C484%2C486%2C488%2C490%2C492%2C494%2C498%2C540%2C665%2C667%2C669%2C671%2C675%2C677%2C679%2C681%2C683%2C685%2C687%2C689%2C691%2C693%2C709%2C719%2C721%2C723%2C6504&classeTreeSelection.text=752+Registros+selecionados&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=&dadosConsulta.dtFim=&varasTreeSelection.values=&varasTreeSelection.text=&dadosConsulta.ordenacao=DESC")
        if response.status_code != req.codes.ok:
            self.logger.info("A url inicial nao pode se encontrada para a thread: %s", str(self.id))
            return 1

        self.extrai_numero_processo(self.id, response)
        for i in range(self.pagInit, self.pagEnd):
            url_t = "http://esaj.tjsp.jus.br/cjpg/trocarDePagina.do?pagina=" + str(i) + "&conversationId="
            self.logger.info("Pagina %s", str(i))
            response = session.get(url_t)
            if response.status_code == req.codes.ok:
                self.extrai_numero_processo(self.id, response)
            else:
                self.logger.info("A url nao pode ser encontrada: %s", str(url_t))
        end = datetime.now()
        print("Took {}s to rund thread {}".format((end - start).total_seconds(), self.id))
        del session

    def run(self):
        self.t1 = threading.Thread(target=self.download)
        self.t1.start()

    def join(self):
        self.t1.join()
        print(self.arquivos)
        #d = DownloadSetence(self.create_driver(), self.arquivos)
        #print("Vai executar o download de arqvuivos")
        #d.download_pdf_sentencas()

    def os_path(self, file_win, file_linux):
        setencas_dir = os.path.dirname(os.path.realpath(__file__))
        if platform.system() == "Linux":
            path_file = os.path.join(setencas_dir, file_linux)
        else:
            path_file = os.path.join(setencas_dir, file_win)
        return path_file

    def create_driver(self):
        path_phantom = self.os_path("phantomjs.exe", "phantomjs")
        if os.path.exists(path_phantom):
            return webdriver.PhantomJS()

        path_chromedriver = os_path("chromedriver.exe", "chromedriver")
        if os.path.exists(path_chromedriver):
            chrome_options = Options()
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--start-maximized");
            chrome_options.add_argument("useAutomationExtension=false")
            return webdriver.Chrome(path_chromedriver, chrome_options=chrome_options)
