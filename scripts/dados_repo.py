import requests
import pandas as pd
import os
from dotenv import load_dotenv
from math import ceil 

load_dotenv()
class DadosRepositorios:

    def __init__(self, owner):
        self.owner = owner
        self.api_base_url = 'https://api.github.com'
        self.access_token = os.getenv("ACESS_TOKEN")
        self.headers = {'Authorization':'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        
    def lista_repositorios(self):
        repos_list = []

        # calculando a quantidade de paginas
        response = requests.get(f'https://api.github.com/users/{self.owner}')
        num_pages = ceil(response.json()['public_repos']/30)

        for page_num in range(1, num_pages + 1):
            try:
                url = f'{self.api_base_url}/users/{self.owner}/repos?page={page_num}'
                response = requests.get(url, headers=self.headers)
                repos_list.append(response.json())
            except:
                repos_list.append(None)
        
        return repos_list

    def nomes_repos(self, repos_list):
        repo_names = []
        for page in repos_list:
            for repo in page:
                try:
                    repo_names.append(repo['name'])
                except:
                    pass
        return repo_names
    
    def nomes_linguagens(self, repos_list):
        repos_language = []

        for page in repos_list:
            for repo in page:
                try:
                    repos_language.append(repo['language'])
                except:
                    pass
        return repos_language
    
    def cria_df_linguagens(self):
        repositorios = self.lista_repositorios()
        nomes = self.nomes_repos(repositorios)
        linguagens = self.nomes_linguagens(repositorios)

        dados = pd.DataFrame()
        dados['repository_name'] = nomes
        dados['language'] = linguagens

        return dados
    
    def salvar_dados(self, dados):
        name_file = f"{self.owner}_github_languages_repos.csv"
        path = f"./dados/{name_file}"
        dados.to_csv(path, index=False)
        print(f"Salvando dados de {self.owner} em {path}")

    
    


amazon_rep = DadosRepositorios('amzn')
languages_amzn = amazon_rep.cria_df_linguagens()
print("-=" * 100)
# print(amazon_rep.lista_repositorios())
# print(languages_amzn)

netflix_rep = DadosRepositorios('netflix')
languages_netflix = netflix_rep.cria_df_linguagens()
print("-=" * 100)
# print(netflix_rep.lista_repositorios())
# print(languages_netflix)

spotify_rep = DadosRepositorios('spotify')
languages_spotify = spotify_rep.cria_df_linguagens()
print("-=" * 100)
# print(spotify_rep.lista_repositorios())
# print(languages_spotify)

apple_rep = DadosRepositorios('apple')
languages_apple = apple_rep.cria_df_linguagens()

# Salvando os dados
amazon_rep.salvar_dados(languages_amzn)
netflix_rep.salvar_dados(languages_netflix)
spotify_rep.salvar_dados(languages_spotify)
apple_rep.salvar_dados(languages_apple)
