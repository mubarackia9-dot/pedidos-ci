# Servidor Jenkins con el cliente de Docker y los plugins del pipeline.
FROM jenkins/jenkins:lts-jdk21

USER root

# Cliente de Docker (y plugin buildx) tomado de la imagen oficial de Docker.
# Jenkins usa el motor de Docker del equipo a través del socket montado.
COPY --from=docker:29-cli /usr/local/bin/docker /usr/local/bin/docker
COPY --from=docker:29-cli /usr/local/libexec/docker/cli-plugins/ /usr/local/libexec/docker/cli-plugins/

# Plugins necesarios para el pipeline (lista en plugins.txt).
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins
