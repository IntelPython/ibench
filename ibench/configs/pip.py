from  ibench.configs.config import Config
import ibench.docker.build as dbuild

class Pip(Config):
    _docker = 'rscohn2/ibench.pip.ubuntu'

    def build(self):
        dbuild.build([{'os_name': 'ubuntu', 'config': 'pip'}])

