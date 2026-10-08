cmake_minimum_required(VERSION 3.15...4.0)
project(
  MixiD
  VERSION 0.1.6
  LANGUAGES CXX)

add_definitions(-DVERSION_MIXID="${MixiD_VERSION}") 
list(APPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_LIST_DIR}/CMake)
INCLUDE(FindPkgConfig)
include(FetchContent) 
FetchContent_Declare(imgui_external
	URL https://github.com/ocornut/imgui/archive/refs/tags/v1.92.4.tar.gz
	EXCLUDE_FROM_ALL
)
FetchContent_MakeAvailable(imgui_external)

add_library(imgui
	${imgui_external_SOURCE_DIR}/imgui.cpp
	${imgui_external_SOURCE_DIR}/imgui_draw.cpp
	${imgui_external_SOURCE_DIR}/imgui_tables.cpp
	${imgui_external_SOURCE_DIR}/imgui_widgets.cpp
	${imgui_external_SOURCE_DIR}/backends/imgui_impl_glfw.cpp
	${imgui_external_SOURCE_DIR}/backends/imgui_impl_opengl3.cpp
)
target_include_directories(imgui PUBLIC ${imgui_external_SOURCE_DIR})
find_package(GLEW REQUIRED)
include_directories(${GLEW_INCLUDE_DIRS})

find_package(OpenGL REQUIRED)
include_directories(${OPENGL_INCLUDE_DIRS})

find_package(LibUSB REQUIRED)
include_directories(${LIBUSB_INCLUDE_DIR})

# convert data into code
include(CMake/bin2h.cmake)
file(GLOB_RECURSE ASSET_FILES CONFIGURE_DEPENDS Assets/*)
file(REMOVE "Raw_Assets.h")

foreach(file ${ASSET_FILES})
	get_filename_component(variableName ${file} NAME)
	message("   ${variableName}")
	list(LENGTH PLUGIN_ASSETLIST ASSET_COUNT)
	message("List size: ${ASSET_COUNT}")
	if (ASSET_COUNT EQUAL 0)
		message("Overwrite")
		bin2h(SOURCE_FILE ${file} HEADER_FILE "Raw_Assets.h" VARIABLE_NAME ${variableName} NULL_TERMINATE)
	else()
		bin2h(SOURCE_FILE ${file} HEADER_FILE "Raw_Assets.h" VARIABLE_NAME ${variableName} APPEND NULL_TERMINATE)
	endif()
	list(APPEND PLUGIN_ASSETLIST ${NEWASSET})
	string(REPLACE ";" "," PLUGIN_ASSETLIST_STRING "${PLUGIN_ASSETLIST}")
endforeach()
message("Converted to C header: ${ASSET_FILES}")

# Adding something we can run - Output name matches target name
add_executable(MixiD main.cpp imgui-knobs.cpp imgui-custom.cpp)

# Make sure you link your targets with this command. It can also link libraries and
# even flags, so linking a target that does not exist will not give a configure-time error.
target_link_libraries(MixiD PRIVATE imgui glfw ${OPENGL_LIBRARIES} ${LIBUSB_LIBRARIES})

include(GNUInstallDirs)

# Install executable
install(TARGETS MixiD DESTINATION ${CMAKE_INSTALL_BINDIR})
install(CODE "file(CREATE_LINK \"MixiD\" \"\$ENV{DESTDIR}\${CMAKE_INSTALL_PREFIX}/${CMAKE_INSTALL_BINDIR}/id-mixer\" SYMBOLIC)")

# Install desktop file
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/desktop/id-mixer.desktop
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/applications)

# Install scalable SVG icon
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/desktop/icons/hicolor/scalable/apps/id-mixer.svg
        DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/icons/hicolor/scalable/apps)

# Install PNG icons for each size
foreach(SIZE 16 32 48 64 128 256 512)
    install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/desktop/icons/hicolor/${SIZE}x${SIZE}/apps/id-mixer.png
            DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/icons/hicolor/${SIZE}x${SIZE}/apps)
endforeach()

# Install udev rules
install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/desktop/84-audient.rules
        DESTINATION /lib/udev/rules.d)

# CPack Packaging configuration
set(CPACK_PACKAGE_NAME "id-mixer")
set(CPACK_PACKAGE_VENDOR "TheOnlyJoey, subigyanpaudel")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Unofficial Linux mixer for Audient iD series audio interfaces")
set(CPACK_PACKAGE_VERSION "${MixiD_VERSION}")
set(CPACK_PACKAGE_CONTACT "subigyanpaudel <https://github.com/subigyanpaudel/MixiD>")
if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE.md")
    set(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/LICENSE.md")
endif()

set(CPACK_GENERATOR "DEB;TGZ")
set(CPACK_SET_DESTDIR ON)
set(CPACK_DEBIAN_PACKAGE_NAME "id-mixer")
set(CPACK_DEBIAN_FILE_NAME DEB-DEFAULT)
set(CPACK_DEBIAN_PACKAGE_MAINTAINER "subigyanpaudel <https://github.com/subigyanpaudel/MixiD>")
set(CPACK_DEBIAN_PACKAGE_SECTION "sound")
set(CPACK_DEBIAN_PACKAGE_PRIORITY "optional")
set(CPACK_DEBIAN_PACKAGE_HOMEPAGE "https://github.com/subigyanpaudel/MixiD")
set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)
set(CPACK_DEBIAN_PACKAGE_CONTROL_EXTRA
    "${CMAKE_CURRENT_SOURCE_DIR}/packaging/postinst;${CMAKE_CURRENT_SOURCE_DIR}/packaging/postrm")

include(CPack)
