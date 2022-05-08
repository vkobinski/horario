import PyPDF2
import re

class Info:
    def __init__(self, arquivo):
        pdfFileObj = open(arquivo, 'rb')

        pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

        pageObj = pdfReader.getPage(0)

        linhas = pageObj.extractText().split("\n")

        codigos = []
        nome_materia = []
        horarios = []
        horarios_tempo = []
        horarios_bruto = []

        disciplinas = []
        ainda_disciplina = False
        ainda_horario = False

        count_horario = 0

        for i, linha in enumerate(linhas):
            if "Turno" in linha:
                ainda_disciplina = True
            if "Professores" in linha:
                ainda_disciplina = False
            if "Segunda" in linha:
                ainda_horario = True
            if ainda_disciplina:
                atual = re.match("[0-9]+-[a-zA-Z]-[0-9]+", linha)
                if atual != None:
                    codigos.append(atual[0].split("-")[0])
                    nome_materia.append(linhas[i+2])
            if ainda_horario:
                atual = re.match("[0-9]+-[a-zA-Z]{3}-[0-9]+|[0-9]+-[a-zA-Z]{1}-[0-9]+", linha)
                if atual != None:
                    horarios.append(atual[0].split("-")[0])
                    match_horario = re.match("[0-9]{2}:[0-9]{2}", linhas[i+2])
                    if match_horario != None:
                        horarios_tempo.append(count_horario)
                        horarios_bruto.append(match_horario[0])
                    match_horario = re.match("[0-9]{2}:[0-9]{2}", linhas[i+1])
                    if match_horario != None:
                        horarios_tempo.append(count_horario)
                        horarios_bruto.append(match_horario[0])
                    count_horario += 1

        self.disciplinas = disciplinas
        self.codigos = codigos
        self.nome_materia = nome_materia
        self.horarios = horarios
        self.horarios_tempo = horarios_tempo
        self.horarios_bruto = horarios_bruto

        pdfFileObj.close()