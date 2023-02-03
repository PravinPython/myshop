from shop import app
import logging as logger


if __name__ == '__main__':
    logger.debug("Starting Flask Server")
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)
