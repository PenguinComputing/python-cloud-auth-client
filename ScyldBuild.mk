ifneq ($(VERBOSE),0)
$(warning parsing python-cloud-auth-client/ScyldBuild.mk)
endif

# Variables need to be unique across the entire build, so prefix them with 
# the directory name.
python-cloud-auth-client_SPEC=python-cloud-auth-client/python-cloud-auth-client.spec
python-cloud-auth-client_ARCHS := x86_64

SPECFILES += $(python-cloud-auth-client_SPEC)

# create a variable storing the list of targets for this make segment
# so that other packages can manually add their own dependencies easily
python-cloud-auth-client_TARGETS += $(call add_targets,python-cloud-auth-client)
BUILD_TARGETS += $(python-cloud-auth-client_TARGETS)
python-cloud-auth-client_INSTALL_RPMS := $(call install_some_rpms,python-cloud-auth-client,'debuginfo')

scyld-python-cloud-auth-client_VERSION := 0.1.1

$(RPM_SOURCE_DIR)/python-cloud-auth-client-$(scyld-python-cloud-auth-client_VERSION).tar.gz: $(shell find python-cloud-auth-client -print -type f)
	( cd python-cloud-auth-client ; tar zcf $@ *)

clean::
	$(RM) $(RPM_SOURCE_DIR)/python-cloud-auth-client-$(scyld-python-cloud-auth-client_VERSION).tar.gz

