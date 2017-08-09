from flask import Blueprint, abort, current_app, jsonify, request, Flask, Response, send_from_directory, redirect, flash, url_for, render_template
from datetime import datetime
import settings

# Rest API
rest_api = Blueprint('rest_api', __name__)
