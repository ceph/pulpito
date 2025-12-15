pulpito
=======
A dashboard for Ceph test runs and results. You can see ours here: http://pulpito.ceph.com/

Setup
=====

#. First, you need a running `paddles <https://github.com/ceph/paddles/>`_ instance
#. Clone the `repository <https://github.com/ceph/pulpito.git>`_
#. Inside the repository, create a virtualenv: ``virtualenv ./virtualenv``
#. Create a copy of the configuration template: ``cp config.py.in prod.py``
#. Edit prod.py to reflect your paddles configuration
#. Activate the virtualenv: ``source ./virtualenv/bin/activate``
#. Install required python packages: ``pip install -r requirements.txt``
#. To start the server, you may use ``python run.py`` - though we use `supervisord <http://supervisord.org/>`_ to manage it. A sample config file is provided for `supervisord <supervisord_pulpito.conf>`_.

Deploying in OpenShift
======================

Pulpito can be built and deployed natively in OpenShift using
``BuildConfig`` and ``ImageStream`` resources.

The repository provides a split layout:

::

    openshift/
      build/
        imagestream.yaml
        buildconfig-binary.yaml
        buildconfig-git.yaml
      deploy/
        namespace.yaml
        deployment.yaml
        service.yaml
        route.yaml

Dockerfile
----------

OpenShift builds use ``Dockerfile.ocp`` at the repository root.
This file is compatible with restricted SCCs and random UIDs.

It also copies ``config.py.in`` to ``prod.py`` so that ``run.py`` can
import it at runtime.

Build Options
-------------

Two build methods are supported.

**1. Build from local directory (binary build)**

Apply build resources::

    oc apply -f openshift/build/

Start a build from your working tree::

    oc -n pulpito start-build bc/pulpito-binary --from-dir=. --follow

**2. Build from an upstream Git branch**

Edit ``openshift/build/buildconfig-git.yaml`` and set::

    spec.source.git.ref: main

Then start the build::

    oc -n pulpito start-build bc/pulpito-git --follow

You may also override the branch or tag per build::

    oc -n pulpito start-build bc/pulpito-git \
      --commit=refs/heads/<branch> --follow

Runtime Deployment
------------------

Apply deployment manifests::

    oc apply -f openshift/deploy/

Restart the deployment after a successful build::

    oc -n pulpito rollout restart deploy/pulpito
    oc -n pulpito rollout status deploy/pulpito

The application is exposed via an OpenShift Route using edge TLS.
HTTP requests are redirected to HTTPS by default.

Accessing the UI
----------------

Retrieve the route hostname::

    oc -n pulpito get route pulpito \
      -o jsonpath='{.spec.host}{"\n"}'

Then open the URL in a browser.

Reverse Proxy Notes
===================

When running behind an external reverse proxy (nginx, Apache, etc.),
ensure the original ``Host`` header is preserved::

    proxy_set_header Host $host;

Failing to do this may cause Pulpito to generate redirects pointing at
the internal OpenShift route hostname.
