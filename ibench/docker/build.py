import argparse
import datetime
from jinja2 import PackageLoader
from jinja2 import Environment
import os
import pkg_resources
import subprocess
import sys


def get_proxies():
    proxies = ''
    for var in ['http_proxy','https_proxy','no_proxy']:
        if var in os.environ:
            proxies += ' --build-arg %s=%s' % (var,os.environ[var])
    return proxies

def docker_build(envs, publish):
    proxies = get_proxies()
    for env in envs:
        dockerfile = dockerfileName(env)
        repo = 'rscohn2/%s' % repoName(env)
        tags = '-t %s' % repo
        command = 'docker build %s %s --file %s .' % (proxies,tags,dockerfile)
        print(command)
        subprocess.check_call(command, shell=True)
        if publish:
            subprocess.check_call('docker login -u $DOCKER_USER -p $DOCKER_PASSWORD',shell=True)
            subprocess.check_call('docker push %s' % repo,shell=True)


def repoName(env):
    return 'ibench.%s.%s' % (env['config'],env['os_name'])

def dockerfileName(env):
    return 'Dockerfile.%s' % repoName(env)

def gen_dockerfiles(envs):
    tpl_env = Environment(loader=PackageLoader('ibench', 'docker'))
    for env in envs:
        with open(dockerfileName(env),'w') as df:
            df.write(tpl_env.get_template('Dockerfile.tpl').render(env))

#os_default = ['centos','ubuntu']
os_default = ['ubuntu']
config_default = ['sys_openblas', 'sys_atlas', 'sys_reference', 'pip']

def parseArgs():
    argParser = argparse.ArgumentParser(description='Build Dockerfiles and images for benchmarking',
                                        formatter_class=argparse.RawDescriptionHelpFormatter)
    argParser.add_argument('--publish', default=False, action='store_true', help='publish on dockerhub')
    argParser.add_argument('--os', default=None, nargs='+',
                           help='operating system for docker image. Default: %s' % os_default)
    argParser.add_argument('--config', default=None, nargs='+',
                           help='python config. Default: %s' % config_default)
    args = argParser.parse_args()
    if not args.os:
        args.os = os_default
    if not args.config:
        args.config = config_default
    return args

def genEnvs(args):
    envs = []
    build_date = datetime.datetime.now().strftime('%c')
    vcs_ref = subprocess.check_output('git rev-parse --short HEAD',shell=True).strip()
    for os in args.os:
        for config in args.config:
            envs.append({'os_name': os, 'config': config, 'build_date': build_date, 'vcs_ref': vcs_ref})
    return envs

def build(envs, publish=False):
    gen_dockerfiles(envs)
    docker_build(envs, publish)

if __name__ == '__main__':
    args = parseArgs()
    envs = genEnvs(args)
    build(envs, args.publish)
