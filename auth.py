
from stytch import Client
from stytch.core.response_base import StytchError
from flask import Flask, request, redirect, url_for, session
from os import environ as env


class Auth:

    def __init__(self):
        self.stytch_client = Client(
            project_id=env.get("STYTCH_PROJECT_ID"),
            secret=env.get("STYTCH_SECRET"),
            environment=env.get('envrionment_v')
        )
        pass



    def get_authenticated_user(self):
      stytch_session = session.get('stytch_session_token')
      if not stytch_session:
          return None

      try:
        resp = self.stytch_client.sessions.authenticate(session_token=stytch_session)
      except StytchError as e:
        # Session has expired or is invalid, clear it
        session.pop("stytch_session_token", None)
        return None

      return resp.user