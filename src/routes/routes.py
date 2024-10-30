from fastapi import APIRouter, HTTPException
import requests
from fastapi.responses import FileResponse
import os


router = APIRouter()


@router.get("/", response_class=FileResponse)
def root():
    file_path = os.path.join(os.path.dirname(__file__), "..", "templates", "index.html")
    return FileResponse(file_path)


@router.get("/api/megasena/filter")
def filter(dz1: str, dz2: str, dz3: str, dz4: str, dz5: str = None, dz6: str = None):

    if not dz1 or not dz2 or not dz3:
        raise HTTPException(
            status_code=400, detail="Pelo menos 3 dezenas são requeridas!"
        )

    url = f"https://loteriascaixa-api.herokuapp.com/api/megasena"
    response = requests.get(url)
    data = response.json()

    todos_os_jogos = []

    for concurso in data:
        todos_os_jogos.append(concurso)

    filtro1 = [numero for numero in todos_os_jogos if dz1 in numero["dezenas"]]
    filtro2 = [numero for numero in filtro1 if dz2 in numero["dezenas"]]
    filtro3 = [numero for numero in filtro2 if dz3 in numero["dezenas"]]

    if dz4:
        filtro4 = [numero for numero in filtro3 if dz4 in numero["dezenas"]]
    else:
        filtro4 = filtro3

    if dz5:
        filtro5 = [numero for numero in filtro4 if dz5 in numero["dezenas"]]
    else:
        filtro5 = filtro4

    if dz6:
        filtro6 = [numero for numero in filtro5 if dz6 in numero["dezenas"]]
    else:
        filtro6 = filtro5

    return filtro6
