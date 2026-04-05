from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer

from catalog.models import AutoParts

my_analyzer = analyzer('my_analyzer',
                       tokenizer=tokenizer('trigram', 'edge_ngram', min_gram=3, max_gram=20),
                       filter=['lowercase']
                       )


@registry.register_document
class PartDocument(Document):
    id = fields.IntegerField()
    name = fields.TextField(analyzer=my_analyzer)
    brand = fields.TextField(analyzer=my_analyzer)
    short_description = fields.TextField(analyzer=my_analyzer)
    cost_price = fields.FloatField()
    selling_price = fields.FloatField()
    features = fields.TextField(analyzer=my_analyzer)
    cars = fields.ObjectField(properties={
        'id': fields.IntegerField()

    })
    subcategory = fields.ObjectField(properties={
        'id': fields.IntegerField()
    })
    documents = fields.FileField()

    class Index:
        name = 'part'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
            'max_ngram_diff': 20
        }

    class Django:
        model = AutoParts
        fields = (
            'quantity', 'warranty', 'condition')
