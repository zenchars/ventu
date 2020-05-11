import logging
from enum import Enum

from falcon import API, media
from pydantic import BaseModel
from spectree import SpecTree, Response


class StatusEnum(str, Enum):
    ok = 'OK'
    error = 'Error'


class ServiceStatus(BaseModel):
    """
    service health status
    """
    inference: StatusEnum
    service: StatusEnum = StatusEnum.ok


def create_app(infer, health_check, req_schema, resp_schema, use_msgpack, config):
    """
    create :class:`falcon` application

    :param infer: model infer function (contains `preprocess`, `inference`, and `postprocess`)
    :param health_check: model health check function (need examples provided in schema)
    :param req_schema: request schema defined with :class:`pydantic.BaseModel`
    :param resp_schema: request schema defined with :class:`pydantic.BaseModel`
    :param bool use_msgpack: use msgpack for serialization or not (default: JSON)
    :param config: configs :class:`ventu.config.Config`
    :return: a :class:`falcon` application
    """
    if use_msgpack:
        handlers = media.Handlers({
            'application/msgpack': media.MessagePackHandler(),
        })
        app = API(media_type='application/msgpack')
        app.req_options.media_handlers = handlers
        app.resp_options.media_handlers = handlers
    else:
        app = API()

    api = SpecTree('falcon', title=config.name, version=config.version)
    logger = logging.getLogger(__name__)

    class Homepage:
        def on_get(self, req, resp):
            logger.debug('return service endpoints')
            resp.media = {
                'health check': {'/health': 'GET'},
                'inference': {'/inference': 'POST'},
                'API document': {'/apidoc/redoc': 'GET', '/apidoc/swagger': 'GET'}
            }

    class HealthCheck:
        @api.validate(resp=Response(HTTP_200=ServiceStatus))
        def on_get(self, req, resp):
            """
            Health check
            """
            status = ServiceStatus(inference=StatusEnum.ok)
            try:
                health_check()
            except AssertionError as err:
                status.inference = StatusEnum.error
                logger.warning(f'Service health check error: {err}')
            logger.debug(str(status))
            resp.media = status.dict()

    class Inference:
        @api.validate(json=req_schema, resp=Response(HTTP_200=resp_schema))
        def on_post(self, req, resp):
            """
            Deep learning model inference
            """
            data = req.context.json
            logger.debug(str(data))
            resp.media = infer(data)

    app.add_route('/', Homepage())
    app.add_route('/health', HealthCheck())
    app.add_route('/inference', Inference())
    api.register(app)
    return app
