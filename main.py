from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import json
import random
import unicodedata
from datetime import datetime

load_dotenv()

PREFIXO = "!"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIXO, intents=intents, help_command=None)

with open("cartas.json", "r", encoding="utf-8") as f:
    cartas = json.load(f)

with open("cartas_raras.json", "r", encoding="utf-8") as f:
    cartas_raras = json.load(f)

try:
    with open("perfis.json", "r", encoding="utf-8") as f:
        perfis = json.load(f)
except FileNotFoundError:
    perfis = {}


SIGNOS = {
    "aries": {"nome": "Áries", "simbolo": "♈", "elemento": "Fogo", "modalidade": "Cardinal", "energia": "Impulso", "planeta": "Marte", "foco": "ação, coragem e iniciativa", "sombra": "pressa, irritação e impulsividade", "frase": "A chama nasce antes do medo.", "conselho": "Aja com coragem, mas não confunda velocidade com direção."},
    "touro": {"nome": "Touro", "simbolo": "♉", "elemento": "Terra", "modalidade": "Fixo", "energia": "Estabilidade", "planeta": "Vênus", "foco": "segurança, prazer e construção", "sombra": "teimosia, apego e resistência à mudança", "frase": "Aquilo que cria raízes também aprende a florescer.", "conselho": "Proteja o que tem valor, mas não transforme conforto em prisão."},
    "gemeos": {"nome": "Gêmeos", "simbolo": "♊", "elemento": "Ar", "modalidade": "Mutável", "energia": "Movimento", "planeta": "Mercúrio", "foco": "comunicação, escolhas e ideias", "sombra": "dispersão, dúvida e excesso mental", "frase": "Toda palavra é uma estrela tentando encontrar órbita.", "conselho": "Organize seus pensamentos antes de seguir todas as vozes ao mesmo tempo."},
    "cancer": {"nome": "Câncer", "simbolo": "♋", "elemento": "Água", "modalidade": "Cardinal", "energia": "Memória", "planeta": "Lua", "foco": "emoções, lar e proteção", "sombra": "carência, nostalgia e defensividade", "frase": "A alma guarda marés que ninguém vê.", "conselho": "Cuide do que sente, mas não permita que o passado governe tudo."},
    "leao": {"nome": "Leão", "simbolo": "♌", "elemento": "Fogo", "modalidade": "Fixo", "energia": "Presença", "planeta": "Sol", "foco": "expressão, autoestima e criação", "sombra": "orgulho, vaidade e necessidade de validação", "frase": "O brilho verdadeiro não pede permissão.", "conselho": "Mostre sua luz, mas lembre-se de que presença não precisa virar imposição."},
    "virgem": {"nome": "Virgem", "simbolo": "♍", "elemento": "Terra", "modalidade": "Mutável", "energia": "Ordem", "planeta": "Mercúrio", "foco": "rotina, análise e aperfeiçoamento", "sombra": "crítica excessiva, controle e autocobrança", "frase": "Até o caos possui detalhes esperando cuidado.", "conselho": "Aperfeiçoe o caminho sem exigir perfeição de si o tempo todo."},
    "libra": {"nome": "Libra", "simbolo": "♎", "elemento": "Ar", "modalidade": "Cardinal", "energia": "Equilíbrio", "planeta": "Vênus", "foco": "relações, escolhas e beleza", "sombra": "indecisão, agradar demais e evitar conflitos", "frase": "Toda harmonia nasce de forças que aprenderam a se ouvir.", "conselho": "Busque paz, mas não abandone sua verdade para manter aparência de equilíbrio."},
    "escorpiao": {"nome": "Escorpião", "simbolo": "♏", "elemento": "Água", "modalidade": "Fixo", "energia": "Transformação", "planeta": "Plutão", "foco": "intensidade, sombra e renascimento", "sombra": "controle, desconfiança e obsessão", "frase": "O abismo também é um útero.", "conselho": "Transforme sem destruir tudo ao redor no processo."},
    "sagitario": {"nome": "Sagitário", "simbolo": "♐", "elemento": "Fogo", "modalidade": "Mutável", "energia": "Expansão", "planeta": "Júpiter", "foco": "fé, liberdade e visão", "sombra": "exagero, fuga e imprudência", "frase": "A flecha conhece o céu antes de tocar o alvo.", "conselho": "Expanda seus horizontes, mas não use a liberdade como fuga da responsabilidade."},
    "capricornio": {"nome": "Capricórnio", "simbolo": "♑", "elemento": "Terra", "modalidade": "Cardinal", "energia": "Estrutura", "planeta": "Saturno", "foco": "disciplina, ambição e responsabilidade", "sombra": "rigidez, frieza e excesso de cobrança", "frase": "O tempo coroa quem suporta a subida.", "conselho": "Construa com firmeza, mas não transforme sua vida inteira em obrigação."},
    "aquario": {"nome": "Aquário", "simbolo": "♒", "elemento": "Ar", "modalidade": "Fixo", "energia": "Ruptura", "planeta": "Urano", "foco": "originalidade, futuro e liberdade mental", "sombra": "distanciamento, rebeldia vazia e frieza emocional", "frase": "Algumas estrelas nascem para quebrar constelações antigas.", "conselho": "Questione padrões, mas não se desconecte das pessoas no processo."},
    "peixes": {"nome": "Peixes", "simbolo": "♓", "elemento": "Água", "modalidade": "Mutável", "energia": "Sonho", "planeta": "Netuno", "foco": "intuição, espiritualidade e sensibilidade", "sombra": "fuga, confusão e excesso de idealização", "frase": "O invisível também sabe tocar a pele.", "conselho": "Confie na intuição, mas mantenha os pés minimamente ancorados na realidade."}
}

EVENTOS_COSMICOS = {
    "eclipse_astral": {
        "nome": "Eclipse Astral",
        "emoji": "🌑",
        "chance": 10,
        "descricao": "As sombras estão mais fortes. Cartas invertidas ganham mais peso.",
        "bonus_raridade": "Eclipse"
    },
    "chuva_de_meteoros": {
        "nome": "Chuva de Meteoros",
        "emoji": "☄️",
        "chance": 15,
        "descricao": "Mudanças rápidas atravessam o céu. Leituras tendem a revelar movimento e ruptura.",
        "bonus_raridade": "Rara"
    },
    "noite_de_polaris": {
        "nome": "Noite de Polaris",
        "emoji": "✨",
        "chance": 12,
        "descricao": "A estrela guia está visível. Leituras favorecem clareza, direção e estabilidade.",
        "bonus_raridade": None
    },
    "conjuncao_do_vazio": {
        "nome": "Conjunção do Vazio",
        "emoji": "🌌",
        "chance": 8,
        "descricao": "Forças ocultas se alinham. Cartas raras têm maior chance de aparecer.",
        "bonus_raridade": "Primordial"
    }
}

COMBINACOES_CARTAS = {
    frozenset(["Sirius", "The Black Moon"]): {
        "nome": "A Verdade Oculta",
        "mensagem": "Uma clareza começa a atravessar uma zona de mistério. Algo que estava escondido pode ser percebido com mais lucidez."
    },
    frozenset(["Antares", "The Void King"]): {
        "nome": "Guerra pelo Controle",
        "mensagem": "Existe tensão entre impulso destrutivo e necessidade de domínio. A leitura alerta para conflitos de poder."
    },
    frozenset(["Supernova", "The Devourer"]): {
        "nome": "Renascimento pela Perda",
        "mensagem": "Algo precisa ser consumido para que uma nova versão possa nascer. A transformação vem depois do desapego."
    },
    frozenset(["Vega", "Nova Lux"]): {
        "nome": "Ascensão Iluminada",
        "mensagem": "A consciência se eleva. Esta combinação aponta para aprendizado espiritual, despertar e expansão interior."
    },
    frozenset(["The Wanderer", "Polaris"]): {
        "nome": "O Caminho e o Norte",
        "mensagem": "Mesmo em uma fase incerta, existe uma direção possível. O desconhecido não está totalmente sem guia."
    },
    frozenset(["Eclipse", "The Veil"]): {
        "nome": "O Véu Escurecido",
        "mensagem": "Nem tudo será revelado de imediato. Há ilusões, segredos ou verdades incompletas influenciando a situação."
    },
    frozenset(["Abyssus", "The Crimson Nebula"]): {
        "nome": "Desejo Abissal",
        "mensagem": "Desejo, magnetismo e obsessão podem estar entrelaçados. A leitura pede cuidado com aquilo que seduz e prende."
    },
    frozenset(["The Black Sun", "The White Abyss"]): {
        "nome": "O Fim Antes da Origem",
        "mensagem": "Uma morte simbólica profunda abre espaço para retorno à essência. Esta é uma combinação rara e poderosa."
    },
    frozenset(["The Cosmic Eye", "The Veil"]): {
        "nome": "A Revelação do Véu",
        "mensagem": "A verdade tenta atravessar uma camada de ilusão. Observe sinais, contradições e aquilo que se repete."
    },
    frozenset(["The Astral Queen", "The Black Moon"]): {
        "nome": "Soberania Lunar",
        "mensagem": "Intuição, mistério e sensibilidade estão amplificados. A resposta pode vir mais pelo sentir do que pela lógica."
    }
}

def detectar_combinacoes(cartas_sorteadas):
    nomes = [carta["nome"] for carta in cartas_sorteadas]
    combinacoes_encontradas = []

    for par, dados in COMBINACOES_CARTAS.items():
        if par.issubset(set(nomes)):
            combinacoes_encontradas.append(dados)

    return combinacoes_encontradas

def evento_cosmico_do_dia():
    data = datetime.now().strftime("%d/%m/%Y")
    random.seed(data)

    rolagem = random.randint(1, 100)
    acumulado = 0

    for chave, evento in EVENTOS_COSMICOS.items():
        acumulado += evento["chance"]

        if rolagem <= acumulado:
            random.seed()
            return chave, evento

    random.seed()
    return None, None


def texto_evento_cosmico():
    chave, evento = evento_cosmico_do_dia()

    if evento is None:
        return "Hoje o céu está silencioso. Nenhum evento cósmico especial está ativo."

    return (
        f"{evento['emoji']} **{evento['nome']}**\n\n"
        f"{evento['descricao']}"
    )

def normalizar_texto(texto):
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(char for char in texto if unicodedata.category(char) != "Mn")


def salvar_perfis():
    with open("perfis.json", "w", encoding="utf-8") as f:
        json.dump(perfis, f, ensure_ascii=False, indent=4)


def obter_perfil(usuario):
    user_id = str(usuario.id)

    if user_id not in perfis:
        perfis[user_id] = {
            "nome": usuario.name,
            "signo": None,
            "signo_chave": None,
            "leituras": 0,
            "cartas": {},
            "energias": {},
            "signos_consultados": {},
            "cooldowns": {},
            "ultima_leitura": None
        }
        salvar_perfis()

    perfil = perfis[user_id]

    perfil.setdefault("signo", None)
    perfil.setdefault("signo_chave", None)
    perfil.setdefault("signos_consultados", {})
    perfil.setdefault("cooldowns", {})

    return perfil


def data_hoje():
    return datetime.now().strftime("%d/%m/%Y")


def semana_atual():
    ano, semana, _ = datetime.now().isocalendar()
    return f"{ano}-semana-{semana}"


def pode_fazer_leitura(usuario, tipo, modo="diario"):
    perfil = obter_perfil(usuario)

    marcador_atual = semana_atual() if modo == "semanal" else data_hoje()

    if perfil["cooldowns"].get(tipo) == marcador_atual:
        return False

    return True

def registrar_cooldown(usuario, tipo, modo="diario"):
    perfil = obter_perfil(usuario)

    marcador_atual = semana_atual() if modo == "semanal" else data_hoje()

    perfil["cooldowns"][tipo] = marcador_atual
    salvar_perfis()


def registrar_leitura(usuario, cartas_sorteadas, signo=None):
    perfil = obter_perfil(usuario)
    perfil["leituras"] += 1
    perfil["ultima_leitura"] = datetime.now().strftime("%d/%m/%Y %H:%M")
    
    if signo:
        perfil["signos_consultados"][signo] = perfil["signos_consultados"].get(signo, 0) + 1
        perfil["ultima_leitura_signo"] = {
        "data": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "signo": signo,
        "cartas": cartas_sorteadas
        }
    for carta in cartas_sorteadas:
        perfil["cartas"][carta["nome"]] = perfil["cartas"].get(carta["nome"], 0) + 1
        perfil["energias"][carta["energia"]] = perfil["energias"].get(carta["energia"], 0) + 1

    salvar_perfis()


def mais_recorrente(dicionario):
    if not dicionario:
        return "Ainda não revelado"
    return max(dicionario, key=dicionario.get)


def sortear_carta_com_raridade():
    chave_evento, evento = evento_cosmico_do_dia()

    chance = random.randint(1, 100)

    if evento and evento["bonus_raridade"] == "Primordial":
        chance -= 8
    elif evento and evento["bonus_raridade"] == "Eclipse":
        chance -= 5
    elif evento and evento["bonus_raridade"] == "Rara":
        chance -= 3

    if chance <= 1:
        pool = {n: d for n, d in cartas_raras.items() if d["raridade"] == "Primordial"}
    elif chance <= 5:
        pool = {n: d for n, d in cartas_raras.items() if d["raridade"] == "Eclipse"}
    elif chance <= 15:
        pool = {n: d for n, d in cartas_raras.items() if d["raridade"] == "Rara"}
    else:
        pool = cartas

    nome = random.choice(list(pool.keys()))
    dados = pool[nome]

    if evento and chave_evento == "eclipse_astral":
        invertida = random.choices([True, False], weights=[70, 30])[0]
    else:
        invertida = random.choice([True, False])

    return {
        "nome": nome,
        "tipo": dados["tipo"],
        "raridade": dados.get("raridade", "Comum"),
        "energia": dados["energia"],
        "palavra": dados["palavra"],
        "frase": dados["frase"],
        "estado": "Invertida 🌑" if invertida else "Normal ✨",
        "interpretacao": dados["invertida"] if invertida else dados["normal"]
    }


def sortear_cartas(quantidade=3):
    resultado = []
    nomes_usados = set()

    while len(resultado) < quantidade:
        carta = sortear_carta_com_raridade()
        if carta["nome"] not in nomes_usados:
            resultado.append(carta)
            nomes_usados.add(carta["nome"])

    return resultado


def gerar_mensagem_procedural(tipo_leitura, posicao, carta, signo_info=None):
    estado_invertido = "Invertida" in carta["estado"]
    raridade = carta.get("raridade", "Comum")

    introducoes = [
        f"Na posição de **{posicao}**, **{carta['nome']}** surge como um sinal de **{carta['energia']}**.",
        f"O vazio revela **{carta['nome']}** em **{posicao}**, trazendo a vibração de **{carta['palavra']}**.",
        f"Para **{posicao}**, a carta **{carta['nome']}** aponta para uma força ligada a **{carta['energia']}**."
    ]

    tons = {
        "geral": "Essa energia influencia sua travessia atual de forma ampla.",
        "semanal": "Durante esta semana, esse sinal pode se manifestar em decisões, encontros ou mudanças sutis.",
        "signo": "Para este signo, a carta mostra a vibração principal do dia.",
        "amor": "No campo afetivo, essa energia fala sobre vínculos, desejos e emoções ocultas.",
        "carreira": "Na vida profissional, essa carta aponta para movimento, estratégia ou bloqueios no caminho.",
        "espiritual": "No plano espiritual, essa força revela algo sobre sua sombra, sua intuição ou sua expansão interior."
    }

    estado_texto = (
        "Como saiu **invertida**, essa energia aparece bloqueada, interna ou distorcida."
        if estado_invertido
        else "Como saiu em posição **normal**, essa mensagem aparece de forma mais direta e acessível."
    )

    raridade_texto = ""
    if raridade == "Primordial":
        raridade_texto = "Por ser **Primordial**, esta carta fala de origem, destino profundo e transformação rara."
    elif raridade == "Eclipse":
        raridade_texto = "Por ser de **Eclipse**, ela indica viradas, ocultamentos e revelações importantes."
    elif raridade == "Rara":
        raridade_texto = "Por ser **Rara**, este sinal merece atenção especial."

    signo_texto = ""
    if signo_info:
        signo_texto = (
            f"Para **{signo_info['nome']}**, signo de **{signo_info['elemento']}**, "
            f"essa carta conversa com temas de **{signo_info['foco']}**. "
            f"Sua sombra possível é **{signo_info['sombra']}**."
        )

    conselho = (
        f"O conselho do Void Astra é observar onde **{carta['palavra']}** aparece na sua vida "
        "e agir sem negar aquilo que já está se tornando evidente."
    )

    partes = [
        random.choice(introducoes),
        tons.get(tipo_leitura, tons["geral"]),
        signo_texto,
        estado_texto,
        carta["interpretacao"],
        raridade_texto,
        conselho
    ]

    return "\n\n".join([p for p in partes if p])


def criar_embed_leitura(titulo, descricao, cartas_sorteadas, posicoes, tipo_leitura="geral", signo_info=None):
    embed = discord.Embed(
        title=titulo,
        description=descricao,
        color=0x2b0f54
    )

    chave_evento, evento = evento_cosmico_do_dia()

    if evento:
        embed.add_field(
            name=f"{evento['emoji']} Evento Cósmico Ativo — {evento['nome']}",
            value=evento["descricao"],
            inline=False
        )

    energias = []

    for i, carta in enumerate(cartas_sorteadas):
        posicao = posicoes[i]
        energias.append(carta["energia"])

        mensagem = gerar_mensagem_procedural(
            tipo_leitura,
            posicao,
            carta,
            signo_info
        )

        texto = (
            f"**Tipo:** {carta['tipo']}\n"
            f"**Raridade:** {carta['raridade']}\n"
            f"**Energia:** {carta['energia']}\n"
            f"**Estado:** {carta['estado']}\n"
            f"**Palavra:** {carta['palavra']}\n\n"
            f"*{carta['frase']}*\n\n"
            f"{mensagem}"
        )

        embed.add_field(
            name=f"{posicao} — {carta['nome']}",
            value=texto,
            inline=False
        )

    energia_dominante = max(set(energias), key=energias.count)

    combinacoes = detectar_combinacoes(cartas_sorteadas)
    texto_combinacoes = ""

    if signo_info:
         sintese = (
        f"**Signo:** {signo_info['simbolo']} {signo_info['nome']}\n"
        f"**Elemento:** {signo_info['elemento']}\n"
        f"**Modalidade:** {signo_info['modalidade']}\n"
        f"**Regente:** {signo_info['planeta']}\n"
        f"**Energia:** {signo_info['energia']}\n"
        f"**Sombra:** {signo_info['sombra']}\n"
        f"**Conselho:** {signo_info['conselho']}\n\n"
        f"A energia dominante desta leitura é **{energia_dominante}**."
    )
    else:
        sintese = (
        f"A energia dominante desta leitura é **{energia_dominante}**.\n\n"
        "O Void Astra sugere interpretar as cartas como partes de uma mesma travessia."
    )

    embed.add_field(
    name="🌌 Síntese do Oráculo",
    value=sintese,
    inline=False
)

if combinacoes:
        for combinacao in combinacoes:
            texto_combinacoes += (
                f"**{combinacao['nome']}**\n"
                f"{combinacao['mensagem']}\n\n"
            )

        embed.add_field(
            name="🔗 Combinação Cósmica Revelada",
            value=texto_combinacoes,
            inline=False
        )

    embed.set_footer(text="Void Astra • O vazio nunca permanece em silêncio.")

    return embed


def resposta_simples(titulo, texto):
    return discord.Embed(title=titulo, description=texto, color=0x2b0f54)


@bot.event
async def on_ready():
    print(f"🌌 {bot.user} despertou no vazio.")

@bot.command()
async def reversigno(ctx):
    perfil = obter_perfil(ctx.author)

    ultima = perfil.get("ultima_leitura_signo")

    if not ultima:
        await ctx.send("Você ainda não possui uma leitura de signo registrada hoje.")
        return

    signo_nome = ultima["signo"]
    cartas_salvas = ultima["cartas"]

    signo_info = None

    for dados in SIGNOS.values():
        if dados["nome"] == signo_nome:
            signo_info = dados
            break

    if signo_info is None:
        await ctx.send("Não consegui recuperar os dados do signo dessa leitura.")
        return

    embed = criar_embed_leitura(
        f"{signo_info['simbolo']} Void Astra — Revisão de {signo_info['nome']}",
        f"Esta é sua última leitura astral registrada em **{ultima['data']}**.",
        cartas_salvas,
        ["Energia do Dia", "Desafio Astral", "Conselho Estelar"],
        "signo",
        signo_info
    )

    await ctx.send(embed=embed)

@bot.command()
async def leitura(ctx):
    if not pode_fazer_leitura(ctx.author, "leitura", "diario"):
        await ctx.send(
            "🔮 Você já fez sua leitura geral hoje. "
            "O Void Astra abrirá esse caminho novamente amanhã."
        )
        return

    cartas_sorteadas = sortear_cartas(3)
    registrar_leitura(ctx.author, cartas_sorteadas)
    registrar_cooldown(ctx.author, "leitura", "diario")

    embed = criar_embed_leitura(
        "🔮 Void Astra — Leitura Geral",
        "As estrelas revelam uma travessia entre passado, presente e futuro.",
        cartas_sorteadas,
        ["Passado", "Presente", "Futuro"],
        "geral"
    )

    await ctx.send(embed=embed)

@bot.command()
async def evento(ctx):
    await ctx.send(embed=resposta_simples("🌌 Evento Cósmico do Dia", texto_evento_cosmico()))

@bot.command()
async def meusigno(ctx, *, signo_nome=None):
    if signo_nome is None:
        await ctx.send("Use `!signos` para ver a lista e depois `!meusigno aries`, por exemplo.")
        return

    chave = normalizar_texto(signo_nome)

    if chave not in SIGNOS:
        await ctx.send("Signo não encontrado. Use `!signos` para ver a lista.")
        return

    perfil = obter_perfil(ctx.author)
    perfil["signo"] = SIGNOS[chave]["nome"]
    perfil["signo_chave"] = chave
    salvar_perfis()

    signo = SIGNOS[chave]

    texto = (
        f"{ctx.author.mention}, seu signo foi definido como "
        f"**{signo['simbolo']} {signo['nome']}**.\n\n"
        f"**Elemento:** {signo['elemento']}\n"
        f"**Modalidade:** {signo['modalidade']}\n"
        f"**Energia:** {signo['energia']}\n\n"
        f"*{signo['frase']}*\n\n"
        "Agora você pode usar apenas `!signo` para receber sua leitura astral."
    )

    await ctx.send(embed=resposta_simples("♈ Signo Definido", texto))


@bot.command()
async def signos(ctx):
    texto = ""
    for dados in SIGNOS.values():
        texto += f"**{dados['simbolo']} {dados['nome']}** — {dados['elemento']} — {dados['energia']}\n"

    await ctx.send(embed=resposta_simples("♈ Signos do Void Astra", texto))

@bot.command()
async def semanal(ctx):
    if not pode_fazer_leitura(ctx.author, "semanal", "semanal"):
        await ctx.send(
            "🌌 Você já recebeu sua leitura semanal. "
            "O Void Astra abrirá uma nova leitura na próxima semana."
        )
        return

    cartas_sorteadas = sortear_cartas(3)
    registrar_leitura(ctx.author, cartas_sorteadas)
    registrar_cooldown(ctx.author, "semanal", "semanal")

    embed = criar_embed_leitura(
        "🌌 Void Astra — Leitura Semanal",
        "O vazio abre os sinais para os próximos dias.",
        cartas_sorteadas,
        ["Energia da Semana", "Desafio", "Conselho"],
        "semanal"
    )

    await ctx.send(embed=embed)


@bot.command()
async def signo(ctx, *, signo_nome=None):
    if not pode_fazer_leitura(ctx.author, "signo", "diario"):
        await ctx.send(
            "🌙 Você já recebeu sua leitura de signo hoje. "
            "O Void Astra abrirá esse caminho novamente amanhã."
        )
        return

    perfil = obter_perfil(ctx.author)

    if signo_nome is None:
        if perfil.get("signo_chave"):
            chave = perfil["signo_chave"]
        else:
            await ctx.send(
                "Você ainda não definiu seu signo.\n"
                "Use `!meusigno aries` ou consulte com `!signo aries`."
            )
            return
    else:
        chave = normalizar_texto(signo_nome)

    if chave not in SIGNOS:
        await ctx.send("Signo não encontrado. Use `!signos`.")
        return

    signo_info = SIGNOS[chave]
    cartas_sorteadas = sortear_cartas(3)

    registrar_leitura(ctx.author, cartas_sorteadas, signo_info["nome"])
    registrar_cooldown(ctx.author, "signo", "diario")

    embed = criar_embed_leitura(
        f"{signo_info['simbolo']} Void Astra — {signo_info['nome']}",
        f"O oráculo abriu uma leitura astral para **{signo_info['nome']}**.",
        cartas_sorteadas,
        ["Energia do Dia", "Desafio Astral", "Conselho Estelar"],
        "signo",
        signo_info
    )

    await ctx.send(embed=embed)


@bot.command()
async def amor(ctx):
    if not pode_fazer_leitura(ctx.author, "amor", "diario"):
        await ctx.send(
            "🖤 Você já fez sua leitura do amor hoje. "
            "O Void Astra abrirá esse caminho novamente amanhã."
        )
        return

    cartas_sorteadas = sortear_cartas(3)
    registrar_leitura(ctx.author, cartas_sorteadas)
    registrar_cooldown(ctx.author, "amor", "diario")

    embed = criar_embed_leitura(
        "🖤 Void Astra — Leitura do Amor",
        "O vazio observa os fios invisíveis entre desejo, afeto e destino.",
        cartas_sorteadas,
        ["Seu Coração", "O Vínculo", "Conselho do Oráculo"],
        "amor"
    )

    await ctx.send(embed=embed)


@bot.command()
async def carreira(ctx):
    if not pode_fazer_leitura(ctx.author, "carreira", "diario"):
        await ctx.send(
            "☄️ Você já fez sua leitura de carreira hoje. "
            "O Void Astra abrirá esse caminho novamente amanhã."
        )
        return

    cartas_sorteadas = sortear_cartas(3)
    registrar_leitura(ctx.author, cartas_sorteadas)
    registrar_cooldown(ctx.author, "carreira", "diario")

    embed = criar_embed_leitura(
        "☄️ Void Astra — Leitura de Carreira",
        "As estrelas analisam seu caminho material, profissional e criativo.",
        cartas_sorteadas,
        ["Caminho Atual", "Obstáculo", "Potencial"],
        "carreira"
    )

    await ctx.send(embed=embed)


@bot.command()
async def espiritual(ctx):
    if not pode_fazer_leitura(ctx.author, "espiritual", "diario"):
        await ctx.send(
            "🌙 Você já fez sua leitura espiritual hoje. "
            "O Void Astra abrirá esse caminho novamente amanhã."
        )
        return

    cartas_sorteadas = sortear_cartas(3)
    registrar_leitura(ctx.author, cartas_sorteadas)
    registrar_cooldown(ctx.author, "espiritual", "diario")

    embed = criar_embed_leitura(
        "🌙 Void Astra — Leitura Espiritual",
        "O oráculo atravessa as camadas ocultas da alma.",
        cartas_sorteadas,
        ["Sua Energia", "Sua Sombra", "Sua Elevação"],
        "espiritual"
    )

    await ctx.send(embed=embed)

@bot.command()
async def perfil(ctx):
    perfil = obter_perfil(ctx.author)

    signo_definido = "Ainda não definido"
    if perfil.get("signo_chave") in SIGNOS:
        s = SIGNOS[perfil["signo_chave"]]
        signo_definido = f"{s['simbolo']} {s['nome']}"

    texto = (
        f"**Viajante:** {ctx.author.mention}\n\n"
        f"**Signo definido:** {signo_definido}\n"
        f"**Total de leituras:** {perfil['leituras']}\n"
        f"**Carta mais recorrente:** {mais_recorrente(perfil['cartas'])}\n"
        f"**Energia dominante:** {mais_recorrente(perfil['energias'])}\n"
        f"**Última leitura:** {perfil['ultima_leitura'] or 'Nenhuma leitura registrada'}"
    )

    await ctx.send(embed=resposta_simples("👤 Perfil Astral", texto))


@bot.command()
async def historico(ctx):
    perfil = obter_perfil(ctx.author)

    if not perfil["cartas"]:
        await ctx.send("Você ainda não possui leituras registradas.")
        return

    cartas_ordenadas = sorted(perfil["cartas"].items(), key=lambda item: item[1], reverse=True)
    texto = ""

    for carta, quantidade in cartas_ordenadas[:10]:
        texto += f"**{carta}** — {quantidade} vez(es)\n"

    await ctx.send(embed=resposta_simples("📜 Histórico do Viajante", texto))


@bot.command()
async def energia(ctx):
    perfil = obter_perfil(ctx.author)

    if perfil["energias"]:
        texto = f"{ctx.author.mention}, sua energia dominante registrada é:\n\n**{mais_recorrente(perfil['energias'])}**"
    else:
        texto = f"{ctx.author.mention}, sua energia simbólica inicial é:\n\n**{random.choice(['Luz Perdida', 'Eclipse Interior', 'Chama Astral', 'Névoa Lunar', 'Órbita Silenciosa', 'Caos Estelar', 'Ascensão Cósmica'])}**"

    await ctx.send(embed=resposta_simples("✨ Energia Atual", texto))


@bot.command()
async def cooldowns(ctx):
    perfil = obter_perfil(ctx.author)
    hoje_atual = data_hoje()
    semana = semana_atual()

    def status(tipo, modo="diario"):
        marcador = semana if modo == "semanal" else hoje_atual
        return "Indisponível" if perfil["cooldowns"].get(tipo) == marcador else "Disponível"

    texto = (
        f"**Leitura geral:** {status('leitura')}\n"
        f"**Signo:** {status('signo')}\n"
        f"**Amor:** {status('amor')}\n"
        f"**Carreira:** {status('carreira')}\n"
        f"**Espiritual:** {status('espiritual')}\n"
        f"**Semanal:** {status('semanal', 'semanal')}"
    )

    await ctx.send(embed=resposta_simples("⏳ Cooldowns do Void Astra", texto))


@bot.command()
async def lore(ctx):
    texto = (
        "Em construção..."
    )

    await ctx.send(embed=resposta_simples("🌌 Lore do Void Astra", texto))


@bot.command()
async def carta(ctx, *, nome_carta=None):
    if nome_carta is None:
        await ctx.send("Use assim: `!carta Sirius`")
        return

    todas_as_cartas = {}
    todas_as_cartas.update(cartas)
    todas_as_cartas.update(cartas_raras)

    encontrada = None

    for nome in todas_as_cartas:
        if nome.lower() == nome_carta.lower():
            encontrada = nome
            break

    if encontrada is None:
        await ctx.send("Carta não encontrada no Void Astra.")
        return

    dados = todas_as_cartas[encontrada]

    texto = (
        f"**Tipo:** {dados['tipo']}\n"
        f"**Raridade:** {dados.get('raridade', 'Comum')}\n"
        f"**Energia:** {dados['energia']}\n"
        f"**Palavra:** {dados['palavra']}\n\n"
        f"*{dados['frase']}*\n\n"
        f"**Normal:** {dados['normal']}\n\n"
        f"**Invertida:** {dados['invertida']}"
    )

    await ctx.send(embed=resposta_simples(f"🎴 {encontrada}", texto))


@bot.command()
async def arcano(ctx):
    arcanos_maiores = [nome for nome, dados in cartas.items() if dados["tipo"] == "Arcano Maior"]
    nome = random.choice(arcanos_maiores)
    dados = cartas[nome]

    texto = (
        f"**Tipo:** {dados['tipo']}\n"
        f"**Raridade:** Comum\n"
        f"**Energia:** {dados['energia']}\n"
        f"**Palavra:** {dados['palavra']}\n\n"
        f"*{dados['frase']}*\n\n"
        f"{dados['normal']}"
    )

    await ctx.send(embed=resposta_simples(f"🌑 Arcano Maior — {nome}", texto))


@bot.command()
async def constelacao(ctx):
    constelacoes = [
        "Orion — propósito, força e perseguição da missão.",
        "Lyra — arte, sensibilidade e transcendência.",
        "Scorpius — intensidade, morte simbólica e renascimento.",
        "Ursa Major — proteção, direção e ancestralidade.",
        "Cygnus — passagem, beleza e transformação.",
        "Draco — poder oculto, defesa e vigilância."
    ]

    await ctx.send(embed=resposta_simples("🌠 Constelação Revelada", random.choice(constelacoes)))


@bot.command()
async def ajuda(ctx):
    texto = (
        "**Comandos de leitura**\n"
        "`!leitura` — leitura geral diária.\n"
        "`!semanal` — leitura semanal.\n"
        "`!signo` — leitura diária do seu signo definido.\n"
        "`!reversigno` — mostra novamente sua última leitura de signo.\n"
        "`!meusigno` — define seu signo pessoal.\n"
        "`!amor` — leitura diária sobre amor.\n"
        "`!carreira` — leitura diária profissional.\n"
        "`!espiritual` — leitura diária espiritual.\n"
        "`!cooldowns` — mostra quais leituras ainda estão disponíveis.\n"
        "`!evento` — mostra o evento cósmico ativo do dia.\n\n"

        "**Comandos do viajante**\n"
        "`!perfil` — mostra seu perfil astral.\n"
        "`!historico` — mostra suas cartas recorrentes.\n"
        "`!energia` — mostra sua energia dominante.\n\n"

        "**Comandos do universo**\n"
        "`!lore` — mostra a história do Void Astra.\n"
        "`!arcano` — sorteia um Arcano Maior.\n"
        "`!constelacao` — revela uma constelação simbólica."
    )

    await ctx.send(embed=resposta_simples("🕯️ Ajuda — Void Astra", texto))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado. Use `!ajuda`.")
    else:
        await ctx.send("Ocorreu um erro ao executar o comando.")
        print(error)

bot.run(os.getenv("DISCORD_TOKEN"))
