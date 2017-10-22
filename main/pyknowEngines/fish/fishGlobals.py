from django.http import HttpRequest
global request
request = HttpRequest()

newFacts = {
    'feature': {
        'method': 'declareFeatures',
        'facts': [
            {'key': 'oldFeatures', 'fustyKey': 'feature',
                'button': 'feature_submit',},
            {'key': 'idunnoFeatures', 'fustyKey': 'newIdunnoFeatures',
                'button': 'feature_idunno',},
            {'key': 'ignoreFeatures', 'fustyKey': 'newIgnoreFeatures',
                'button': 'feature_no',},
        ]
    },
    'kind': {
        'method': 'declareKinds',
        'facts': [
            {'key': 'oldKinds', 'fustyKey': 'kind',
                'button': 'kind_submit',},
            {'key': 'idunnoKinds', 'fustyKey': 'newIdunnoKinds',
                'button': 'kind_idunno',},
            {'key': 'ignoreKinds', 'fustyKey': 'newIgnoreKinds',
                'button': 'kind_no',},
        ]
    },
    'detachment': {
        'method': 'declareDetachments',
        'facts': [
            {'key': 'oldDetachments', 'fustyKey': 'detachment',
                'button': 'detachment_submit',},
            {'key': 'idunnoDetachments', 'fustyKey': 'newIdunnoDetachments',
                'button': 'detachment_idunno',},
            {'key': 'ignoreDetachments', 'fustyKey': 'newIgnoreDetachments',
                'button': 'detachment_no',},
        ]
    }
}


# # TODO: uncomment and fix work with newFacts
# global newFacts
# newFacts = {}
# def newFactsRegister(className):
#     global newFacts
#     lowerName = className.lower()
#     newFacts[className.lower()] = {
#         'method': 'declare{}'.format(className),
#         'facts': [
#             {
#                 'key': 'old{}'.format(className),
#                 'fustyKey': lowerName,
#                 'button': '{}_submit'.format(lowerName),
#             },
#             {
#                 'key': 'idunno{}'.format(className),
#                 'fustyKey': 'newIdunno{}'.format(className),
#                 'button': '{}_idunno'.format(lowerName),
#             },
#             {
#                 'key': 'ignore{}'.format(className),
#                 'fustyKey': 'newIgnore{}'.format(className),
#                 'button': '{}_no'.format(lowerName),
#             },
#         ]
#     }
