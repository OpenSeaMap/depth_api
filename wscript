APPNAME = 'openseamap-api'
VERSION = '1.1'


top = '.'
out = 'build'


def configure(ctx):
    ctx.env.PREFIX = './out'
    ctx.recurse('docs')
    ctx.recurse('install')
    ctx.recurse('src')


def build(ctx):
    ctx.recurse('docs')
    ctx.recurse('install')
    ctx.recurse('src')
