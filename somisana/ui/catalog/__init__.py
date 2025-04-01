from pathlib import Path

from flask import Flask

from somisana.config import somisana_config
from somisana.const import SOMISANAScope
from odp.const import ODPScope
from somisana.ui.catalog import views
from odp.const.hydra import HydraScope
from somisana.version import VERSION
from odp.ui import base


def create_app():
    """
    Flask application factory.
    """
    app = Flask(__name__)
    app.config.update(
        UI_CLIENT_ID=somisana_config.SOMISANA.CATALOG.UI_CLIENT_ID,
        UI_CLIENT_SECRET=somisana_config.SOMISANA.CATALOG.UI_CLIENT_SECRET,
        UI_CLIENT_SCOPE=[
            HydraScope.OPENID,
            HydraScope.OFFLINE_ACCESS,
            # SADCOScope.HYDRO_DOWNLOAD,
            # SADCOScope.CURRENTS_DOWNLOAD,
            # SADCOScope.WEATHER_DOWNLOAD,
            # SADCOScope.WAVES_DOWNLOAD,
            # SADCOScope.UTR_DOWNLOAD,
            # SADCOScope.VOS_DOWNLOAD,
            # SADCOScope.DOWNLOAD_READ,
            # SADCOScope.DOWNLOAD_ADMIN,
            ODPScope.TOKEN_READ
        ],
        CI_CLIENT_ID=somisana_config.SOMISANA.CATALOG.CI_CLIENT_ID,
        CI_CLIENT_SECRET=somisana_config.SOMISANA.CATALOG.CI_CLIENT_SECRET,
        CI_CLIENT_SCOPE=[
            # SADCOScope.SURVEYS_READ,
            # SADCOScope.HYDRO_READ,
            # SADCOScope.CURRENTS_READ,
            # SADCOScope.WEATHER_READ,
            # SADCOScope.WAVES_READ,
            # SADCOScope.UTR_READ,
            # SADCOScope.ECHO_SOUNDING_READ,
            # SADCOScope.UNKNOWN_READ,
            # SADCOScope.VOS_READ
        ],
        SECRET_KEY=somisana_config.SOMISANA.CATALOG.FLASK_SECRET,
        CATALOG_TERMS_OF_USE='''
                I agree that any extracted data will be used
                for research, non-commercial purposes only, and that data will not be passed to
                a 3rd party. The following acknowledgement should be used in any products:
                'The data has been supplied by the Southern African Data Centre for Oceanography'.
            ''',
        SOMISANA_VERSION=VERSION
    )

    base.init_app(app, user_api=True, client_api=True, template_dir=Path(__file__).parent / 'templates',
                  macro_dir=Path(__file__).parent / 'macros', api_url=somisana_config.SOMISANA.API_URL)

    views.init_app(app)

    return app
