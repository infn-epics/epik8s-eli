
FROM michelo/docker-edm
COPY GUI/  /home/iGp/iGp

COPY config /home/iGp/iGp
COPY entrypoint.sh /tmp

ENV IGPTOP=/home/iGp/iGp
ENV BPMTYPE=LiberaBrilliance
ENV DEVICE=L2
ENV EPICS_BASE=/home/iGp/iGp/base
RUN mkdir -p /home/libera/epics/; ln -sf $EPICS_BASE /home/libera/epics/base-3.14.12.2;cp /home/iGp/iGp/extensions/lib/linux-x86/*.so $EPICS_BASE/lib/linux-x86/;c
WORKDIR /home/iGp/iGp
ENTRYPOINT ["/tmp/entrypoint.sh"]
