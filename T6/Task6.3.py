import select
import socket






def handle_writables(writables):

    # Данное событие возникает когда в буффере на запись освобождается место
    for resource in writables:
        try:
            resource.send(bytes('Hello from server!', encoding='UTF-8'))
        except OSError:
            clear_resource(resource)

