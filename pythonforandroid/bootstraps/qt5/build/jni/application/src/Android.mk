LOCAL_PATH := $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := main

# LOCAL_C_INCLUDES := $(LOCAL_PATH)/$(SDL_PATH)/include

# Add your application source files here...
LOCAL_SRC_FILES := start.c pyjniusjni.c

LOCAL_CFLAGS += -I$(PYTHON_INCLUDE_ROOT) $(EXTRA_CFLAGS)

#LOCAL_SHARED_LIBRARIES := python_shared
LOCAL_SHARED_LIBRARIES := python3.8

LOCAL_LDLIBS := -llog -ldl $(EXTRA_LDLIBS)

LOCAL_LDFLAGS += -L$(PYTHON_LINK_ROOT) $(APPLICATION_ADDITIONAL_LDFLAGS)

include $(BUILD_SHARED_LIBRARY)
