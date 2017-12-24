import json
import click
from elasticsearch import Elasticsearch

#tell Click that the following function is going to be exposed as a command-line root
@click.command()
#declare mandatory arguments
@click.argument('query', required=True)
#declare optional arguments
@click.option('--raw-result/--no-raw-result', default=False)

#parameter names should match arguments name above for click function
def search(query, raw_result):
    es = Elasticsearch()
    #search for the query in 'mail' index(database)
    matches = es.search('mail', q=query)
    #grab hits from elasticsearch result
    hits = matches['hits']['hits']
    #check if nothing is found matching the query
    if not hits:
        click.echo('No matches found')
    else:
        #if found, check if user has requested a raw result
        if raw_result:
            click.echo(json.dumps(matches, indent = 4))
        for hit in hits:
            #getting only the main subject lines and the paths of the meta files
            click.echo('Subject: {}\nPath: {}\n\n'.format(
                hit['_source']['subject'],
                hit['_source']['path']
            ))

if __name__ == '__main__':
    search()