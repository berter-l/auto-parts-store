from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer

from blog.models import Article

my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=3, max_gram=20),
                       filter=['lowercase']
                       )


@registry.register_document
class ArticleDocument(Document):
    id = fields.IntegerField()
    title = fields.TextField(analyzer=my_analyzer)
    content = fields.TextField(analyzer=my_analyzer)

    class Index:
        name = 'blog'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_ngram_diff': 20
        }

    class Django:
        model = Article
