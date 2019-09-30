import daiquiri.core.env as env

OAI_SCHEMA = env.get('OAI_SCHEMA', 'oai_schema')

OAI_ADAPTER = 'daiquiri.metadata.adapter.RegistryDoiMetadataOaiAdapter'
OAI_ADMIN_EMAILS = ['admin@example.com']
OAI_METADATA_FORMATS = [
    {
        'prefix': 'oai_dc',
        'schema': 'http://www.openarchives.org/OAI/2.0/oai_dc.xsd',
        'namespace': 'http://www.openarchives.org/OAI/2.0/oai_dc/',
        'renderer_class': 'daiquiri.oai.renderers.DublincoreRenderer'
    },
    {
        'prefix': 'oai_datacite',
        'schema': 'http://schema.datacite.org/oai/oai-1.1/oai.xsd',
        'namespace': 'http://schema.datacite.org/oai/oai-1.1/',
        'renderer_class': 'daiquiri.oai.renderers.OaiDataciteRenderer'
    },
    {
        'prefix': 'datacite',
        'schema': 'http://schema.datacite.org/meta/nonexistant/nonexistant.xsd',
        'namespace': 'http://datacite.org/schema/nonexistant',
        'renderer_class': 'daiquiri.oai.renderers.DataciteRenderer'
    },
    {
        'prefix': 'ivo_vor',
        'schema': 'http://www.ivoa.net/xml/RegistryInterface/v1.0',
        'namespace': 'http://www.ivoa.net/xml/RegistryInterface/v1.0',
        'renderer_class': 'daiquiri.oai.renderers.VoresourceRenderer'
    }
]
OAI_DELETED_RECORD = 'transient'
OAI_GRANULARITY = 'YYYY-MM-DD'
OAI_PAGE_SIZE = 500
