from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pathlib import Path
import json
from models.base_model.base_model import PlaylistBaseModel


app = FastAPI()


class Song(BaseModel):
    song_id: str


class Playlist(BaseModel):
    songs: List[Song]


class Response(BaseModel):
    playlists: List[Playlist]


def generate_response(json):
    playlists = []
    model_response = json
    for playlist in model_response:
        songs = [Song(song_id=x) for x in playlist]
        playlists.append(Playlist(songs=songs))
    response = Response(playlists=playlists)
    return response


@app.get('/')
async def init():
    response = {}
    base_response_path = Path('./responses/base_response.json')
    target_response_path = Path('./responses/target_response.json')
    if not base_response_path.is_file():
        base_response = PlaylistBaseModel().generate_playlists()
        with open('./responses/base_response.json', 'w') as handler:
            json.dump(base_response, handler, indent=3)
        response["Base Model"] = "Initialized successfully"
    if not target_response_path.is_file():
        #target_response = generate_response(PlaylistBaseModel())
        #with open('./responses/target_response.json', 'w') as handler:
        #    json.dump(dict(target_response), handler, indent=3)
        #response["Target Model"] = "Initialized successfully"
        pass
    return response


@app.get('/update')
async def update():
    response = {}
    base_response_path = Path('./responses/base_response.json')
    target_response_path = Path('./responses/target_response.json')
    if base_response_path.is_file():
        base_response = generate_response(PlaylistBaseModel())
        with open('./responses/base_response.json', 'w') as handler:
            json.dump(base_response, handler, indent=3)
        response["Base Model"] = "Updated successfully"
    else:
        response["Base Model"] = "Could not find response file"
    if not target_response_path.is_file():
        #target_response = generate_response(PlaylistBaseModel())
        #with open('./responses/target_response.json', 'w') as handler:
        #    json.dump(dict(target_response), handler, indent=3)
        #response["Target Model"] = "Updated successfully"
        pass
    else:
        #response["Target Model"] = "Could not find response file"
        pass
    return response


@app.get('/base-model')
async def get_base_predictions():
    base_response_path = Path('./responses/base_response.json')
    if base_response_path.is_file():
        with open('./responses/base_response.json', 'r') as handler:
            base_response_json = json.load(handler)
        base_response = generate_response(base_response_json)
    return base_response
    

@app.get('/target-model')
async def get_target_predictions():
    target_response_path = Path('./responses/target_response.json')
    if target_response_path.is_file():
        with open('./responses/target_response.json', 'r') as handler:
            target_response_json = json.load(handler)
        target_response = generate_response(target_response_json)
    return target_response


@app.get('/ab-test')
async def get_ab_test():
    pass


@app.get('/target-test')
async def get_target_test():
    pass
