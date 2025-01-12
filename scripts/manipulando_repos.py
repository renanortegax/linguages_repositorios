import requests
import base64
import os
from dotenv import load_dotenv

class AtualizarRepositorio:
    def __init__(self, username):
        self.username = username
        self.api_base_url = 'https://api.github.com'
        self.access_token = os.getenv("ACESS_TOKEN")
        self.headers = {'Authorization':'Bearer ' + self.access_token,
                        'X-GitHub-Api-Version': '2022-11-28'}
        
    def criar_repo(self, nome_repo, descricao):
        data = {
                    'name': nome_repo,
                    'description': descricao,
                    'private': False
                }
        response = requests.post(f"{self.api_base_url}/users/repos",
                                 json=data, headers=self.headers)

        print(f"status_code criação do repositório: {response.status_code}")

    def add_arquivo(self, nome_repo, nome_arquivo, caminho_arquivo, commit_mesage):
        # Transformar pra binário
        with open(caminho_arquivo, 'rb') as file:
            file_content = file.read()
        encoded_content = base64.b64encode(file_content)
        
        # Enviando o arq
        url = f"{self.api_base_url}/repos/{self.username}/{nome_repo}/contents/{nome_arquivo}"
        data = {
                    "message": commit_mesage,
                    "content": encoded_content.decode("utf-8")
                }
        
        response = requests.put(url, json=data, headers=self.headers)
        print(f"status_code envio do arquivo: {response.status_code}")


# instanciando um objeto
novo_repo = AtualizarRepositorio('renanortegax')

# Criando o repositório
nome_repo = 'linguages_repositorios'
# novo_repo.criar_repo(nome_repo, descricao="Linguagens de repositorios do github")

# Adicionando arquivos salvos no repositório criado
novo_repo.add_arquivo(nome_repo, 'amzn_github_languages_repos.csv', 'dados/amzn_github_languages_repos.csv', commit_mesage="Adicinoando arquivo")
novo_repo.add_arquivo(nome_repo, 'netflix_github_languages_repos.csv', 'dados/netflix_github_languages_repos.csv', commit_mesage="Adicinoando arquivo")
novo_repo.add_arquivo(nome_repo, 'spotify_github_languages_repos.csv', 'dados/spotify_github_languages_repos.csv', commit_mesage="Adicinoando arquivo")