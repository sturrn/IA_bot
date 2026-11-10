from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
 
frases = [
    #saudacoes
    "ola",
    "oi",
    "ola como vai",
    "eai tudo bem",
    "boa tarde",
    "bom dia",
    "boa noite",
    "fala ai",
    "eae",
    "oi tudo bem",
    
    #endereco
    "onde voces estao localizados",
    "onde fica ai",
    "como chego no seu estabelecimento",
    "como chegar ate voces",
    "me passa o endereco",
    "como encontro seu pet shop",
    "onde esta localizado a loja",
    "passa a localizacao suas",
    #BANHO
    "quero dar um banho no meu cachorro",
    "meu cachorro precisa de banho",
    "voces fazem banho em animais",
    "pode lavar o meu cachorro",
    "quero agendar uma ducha",
    "tem serviço de banho",
    "voces dao banho em caes",
    "queria contratar um banho pro meu doguinho",
        # TOSA
    "quero tosar meu cachorro",
    "quanto custa uma tosa",
    "vocês fazem tosa",
    "preciso cortar o pelo do meu cachorro",
    "quero fazer uma tosa higiênica",
    "meu cachorro precisa cortar o pelo",
    "tem serviço de tosa",
    "gostaria de tosar meu pet",
 
    # ESPÉCIES
    "vocês atendem gatos",
    "aceitam gatos no pet shop",
    "quais animais vocês atendem",
    "vocês cuidam de cachorros",
    "posso levar meu gato",
    "atendem outros animais",
    "o pet shop atende cães e gatos",
    "quais espécies vocês recebem",
 
    # AGENDAMENTO
    "quero agendar um horário",
    "como faço para marcar atendimento",
    "preciso marcar um horário",
    "quero fazer um agendamento",
    "tem horário disponível",
    "como faço para agendar",
    "quero reservar um horário",
    "posso marcar um atendimento",
 
    # FUNCIONAMENTO
    "qual o horário de funcionamento",
    "que horas vocês abrem",
    "que horas vocês fecham",
    "vocês abrem aos sábados",
    "a loja funciona no domingo",
    "qual o horário de atendimento",
    "vocês estão abertos hoje",
    "quando o pet shop funciona",
 
    # DESPEDIDAS
    "tchau",
    "até logo",
    "até mais",
    "obrigado pela ajuda",
    "valeu até mais",
    "adeus",
    "obrigado",
    "tenha um bom dia"
]
 
intencao = [
    "saudacao", "saudacao", "saudacao", "saudacao", "saudacao", "saudacao", "saudacao", "saudacao","saudacao", "saudacao",
    "endereco", "endereco", "endereco", "endereco", "endereco", "endereco", "endereco", "endereco",
    "banho", "banho", "banho", "banho", "banho", "banho", "banho", "banho",
    "tosa", "tosa", "tosa", "tosa",
    "tosa", "tosa", "tosa", "tosa",
    "especies", "especies", "especies", "especies",
    "especies", "especies", "especies", "especies",
    "agendamento", "agendamento", "agendamento", "agendamento",
    "agendamento", "agendamento", "agendamento", "agendamento",
    "funcionamento", "funcionamento", "funcionamento", "funcionamento",
    "funcionamento", "funcionamento", "funcionamento", "funcionamento",
    "despedida", "despedida", "despedida", "despedida",
    "despedida", "despedida", "despedida", "despedida"
]
 
df = pd.DataFrame({
    "frase": frases,
    "intencoes": intencao
})
X = df["frase"]
y = df["intencoes"]
 
X_treino, X_teste, y_treino, y_teste = train_test_split(X,y,test_size=0.25, random_state=42, stratify=y)
 
vetor = CountVectorizer(lowercase=True, strip_accents="unicode")
X_treino = vetor.fit_transform(X_treino)
X_teste = vetor.transform(X_teste)
 
modelo = MultinomialNB()
modelo.fit(X_treino, y_treino)
previsao = modelo.predict(X_teste)
acuracia = accuracy_score(y_teste, previsao)
print(f"Acuracia: {acuracia * 100:.2f}%")
 
respostas = {
    "saudacao":
    "Olá! Seja bem-vindo. Como posso ajudar?😊",
    "endereco": "Estamos localizados na rua ABC, n° 123, Bairro Centro.",
    "banho": "Nós temos serviços de banho para cães e gatos. Entre em contato para agendar!😄",
    "tosa": "Realizamos a tosa completa para o seu pet. Venha agendar.",
    "especies":"Nosso pet shop atende cães e gatos!",
    "agendamento":"Para agendar um atendimento, entre em contato com nossa equipe!",
    "funcionamento":"Funcionamos de segunda a sábado, das 8h às 18h.",
    "despedida":"Foi um prazer conversar com você! Até a próxima!"
}
  
def responder(mensagem):
    entrada = vetor.transform([mensagem])
    intencoes = modelo.predict(entrada)[0]
    probabilidade = modelo.predict_proba(entrada)[0]
    confianca = max(probabilidade)
    if confianca < 0.15:
        return "Desculpe, não entendi sua mensagem :("
    resposta = respostas[intencoes]
    return resposta
 
class Servidor(BaseHTTPRequestHandler):
 
    def enviar_json(self, dados, status=200):
        resposta = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", len(resposta))
        self.end_headers()
        self.wfile.write(resposta)
 
    def enviar_arquivo(self, nome, tipo):
        try:
            with open(nome, "rb") as arquivo:
                conteudo = arquivo.read()
 
            self.send_response(200)
            self.send_header("Content-Type", tipo)
            self.send_header("Content-Length", len(conteudo))
            self.end_headers()
            self.wfile.write(conteudo)
 
        except FileNotFoundError:
            self.send_error(404, "Arquivo não encontrado")
 
    def do_GET(self):
        arquivos = {
            "/": ("index.html", "text/html"),
            "/style.css": ("style.css", "text/css"),
            "/script.js": ("script.js", "application/javascript")
        }
 
        if self.path in arquivos:
            nome, tipo = arquivos[self.path]
            self.enviar_arquivo(nome, tipo)
        else:
            self.send_error(404, "Página não encontrada")
 
    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404, "Rota não encontrada")
            return
 
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
 
            if tamanho <= 0 or tamanho > 10000:
                self.enviar_json({"erro": "Mensagem inválida."}, 400)
                return
 
            dados = json.loads(self.rfile.read(tamanho))
            mensagem = dados.get("mensagem", "")
 
            if not isinstance(mensagem, str) or not mensagem.strip():
                self.enviar_json({"erro": "Digite uma mensagem."}, 400)
                return
 
            if len(mensagem) > 500:
                self.enviar_json({"erro": "A mensagem é muito longa."}, 400)
                return
 
            resposta = responder(mensagem)
            self.enviar_json({"resposta": resposta})
 
        except (ValueError, TypeError, json.JSONDecodeError):
            self.enviar_json({"erro": "Não foi possível interpretar a mensagem."}, 400)
 
        except Exception:
            self.enviar_json({"erro": "Ocorreu um erro no chatbot."}, 500)
 
 
servidor = HTTPServer(("127.0.0.1", 8000), Servidor)
print("Servidor em http://127.0.0.1:8000")
servidor.serve_forever()