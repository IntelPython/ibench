from  .config import Config
from  ..docker.build import build as dbuild

class Pip(Config):
    _docker = 'rscohn2/ibench.shared.ubuntu'

    def build(self):
        dbuild([{'os_name': 'ubuntu', 'config': 'shared'}])

