from pythonforandroid.recipe import BootstrapNDKRecipe
from pythonforandroid.toolchain import Recipe, current_directory
from pythonforandroid.logger import info, debug, shprint, warning
from os.path import join, isdir, isfile
from os import environ
from multiprocessing import cpu_count
import sh
import glob


class Qt5Recipe(BootstrapNDKRecipe):
    name = 'qt5'
    url = 'git+http://code.qt.io/qt/qt5.git'
    #version = '5.15.2'
    version = '9b43a43ee96198674060c6b9591e515e2d27c28f'

    dir_name = 'qt5'

    built_libraries = {'dummy':'.'}

    depends = ['python3']
    conflicts = ['sdl2', 'genericndkbuild']

    need_stl_shared = True


    # override as we can't statically define the libs due to arch in filename
    def get_libraries(self, arch_name, in_context=False):
        # TODO: don't hardcode, infer from build config
        self.built_libraries = {
            f'libQt5Core_{arch_name}.so': 'qtbase/lib',
            f'libQt5Gui_{arch_name}.so': 'qtbase/lib',
            f'libQt5Network_{arch_name}.so': 'qtbase/lib',
            f'libQt5Xml_{arch_name}.so': 'qtbase/lib',
            f'libQt5Concurrent_{arch_name}.so': 'qtbase/lib',
            f'libQt5Sql_{arch_name}.so': 'qtbase/lib',
            f'libQt5Qml_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QmlModels_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QmlWorkerScript_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5Quick_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickShapes_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickParticles_{arch_name}.so': 'qtdeclarative/lib',
            f'libQt5QuickTemplates2_{arch_name}.so': 'qtquickcontrols2/lib',
            f'libQt5QuickControls2_{arch_name}.so': 'qtquickcontrols2/lib',
            f'libQt5RemoteObjects_{arch_name}.so': 'qtremoteobjects/lib',
            f'libQt5Multimedia_{arch_name}.so': 'qtmultimedia/lib',
            f'libQt5MultimediaQuick_{arch_name}.so': 'qtmultimedia/lib',

            f'libplugins_bearer_qandroidbearer_{arch_name}.so': 'qtbase/plugins/bearer',
            f'libplugins_platforms_qtforandroid_{arch_name}.so': 'qtbase/plugins/platforms',
            f'libplugins_imageformats_qjpeg_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qico_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qgif_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qtga_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qtiff_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qwebp_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qicns_{arch_name}.so': 'qtimageformats/plugins/imageformats',
            f'libplugins_imageformats_qwbmp_{arch_name}.so': 'qtimageformats/plugins/imageformats',

            f'libplugins_playlistformats_qtmultimedia_m3u_{arch_name}.so': 'qtmultimedia/plugins/playlistformats',
            f'libplugins_video_videonode_qtsgvideonode_android_{arch_name}.so': 'qtmultimedia/plugins/video/videonode',
            f'libplugins_mediaservice_qtmedia_android_{arch_name}.so': 'qtmultimedia/plugins/mediaservice',
            f'libplugins_audio_qtaudio_opensles_{arch_name}.so': 'qtmultimedia/plugins/audio',

            f'libplugins_qmltooling_qmldbg_preview_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_native_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_debugger_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_local_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_messages_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_quickprofiler_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_nativedebugger_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_server_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_tcp_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_inspector_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_profiler_{arch_name}.so': 'qtdeclarative/plugins/qmltooling',

            f'libqml_QtQml_qmlplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml',
            f'libqml_QtQml_WorkerScript.2_workerscriptplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml/WorkerScript.2',
            f'libqml_QtQml_StateMachine_qtqmlstatemachine_{arch_name}.so': 'qtdeclarative/qml/QtQml/StateMachine',
            f'libqml_QtQml_Models.2_modelsplugin_{arch_name}.so': 'qtdeclarative/qml/QtQml/Models.2',
            f'libqml_QtQuick_Window.2_windowplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Window.2',
            f'libqml_QtQuick_Layouts_qquicklayoutsplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Layouts',
            f'libqml_QtQuick_Shapes_qmlshapesplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/Shapes',
            f'libqml_QtQuick.2_qtquick2plugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick.2',
            f'libqml_QtQuick_LocalStorage_qmllocalstorageplugin_{arch_name}.so': 'qtdeclarative/qml/QtQuick/LocalStorage',
            f'libqml_QtQuick_Templates.2_qtquicktemplates2plugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Templates.2',
            f'libqml_QtQuick_Controls.2_qtquickcontrols2plugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Controls.2',
            f'libqml_QtQuick_Controls.2_Material_qtquickcontrols2materialstyleplugin_{arch_name}.so': 'qtquickcontrols2/qml/QtQuick/Controls.2/Material',
            f'libqml_QtRemoteObjects_qtremoteobjects_{arch_name}.so': 'qtremoteobjects/qml/QtRemoteObjects',
            f'libqml_QtGraphicalEffects_qtgraphicaleffectsplugin_{arch_name}.so': 'qtgraphicaleffects/qml/QtGraphicalEffects',
            f'libqml_QtGraphicalEffects_private_qtgraphicaleffectsprivate_{arch_name}.so': 'qtgraphicaleffects/qml/QtGraphicalEffects/private',
            f'libqml_QtMultimedia_declarative_multimedia_{arch_name}.so': 'qtmultimedia/qml/QtMultimedia',
        }
        return super().get_libraries(arch_name, in_context)

    def get_recipe_env(self, arch=None, with_flags_in_cc=True, with_python=True):
        env = super().get_recipe_env(
            arch=arch, with_flags_in_cc=with_flags_in_cc,
            with_python=with_python,
        )
        env['APP_ALLOW_MISSING_DEPS'] = 'true'
        env['TARGET_QMAKEPATH'] = join(self.ctx.libs_dir, 'bin')

        return env

    def build_arch(self, arch):
        super().build_arch(arch)

        env = self.get_recipe_env(arch)
        with current_directory(self.get_jni_dir()):
            shprint(sh.ndk_build, "V=1", _env=env, _critical=True)

        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            info("compiling qt5 from sources")
            debug("environment: {}".format(env))

            info("NDK sysroot: %s" % self.ctx.ndk_sysroot)
            info("libdir: %s" % join(build_dir, 'obj', 'local', arch.arch))

            configure = sh.Command('./configure')
            # options?
            shprint(configure, '--help', _env=env, _tail=50, _critical=True)

            configure = configure.bake('-opensource', '-confirm-license', '-disable-rpath')
            configure = configure.bake('-android-sdk', self.ctx.sdk_dir)
            configure = configure.bake('-android-ndk', self.ctx.ndk_dir)
            configure = configure.bake('-xplatform', 'android-clang')
            configure = configure.bake('-android-abis', arch.arch)
            configure = configure.bake('-extprefix', self.ctx.libs_dir)
            configure = configure.bake('-nomake', 'tests')
            configure = configure.bake('-nomake', 'examples')
            configure = configure.bake('-no-widgets')

            # openssl
            openssl = Recipe.get_recipe('openssl', self.ctx)
            configure = configure.bake('-ssl', '-openssl-runtime')
            configure = configure.bake('OPENSSL_INCDIR=' + join(openssl.get_build_dir(arch.arch), 'include'))
            configure = configure.bake('OPENSSL_LIBDIR=' + openssl.get_build_dir(arch.arch))
            configure = configure.bake('OPENSSL_LIBS=%s' % openssl.link_libs_flags().strip())

            for exclude in "quickcontrols2-fusion quickcontrols2-imagine quickcontrols2-universal".split(' '):
                configure = configure.bake('-no-feature-%s' % exclude)

            info(str(configure))

            shprint(configure, _tail=50, _critical=True)

            shprint(sh.make, '-j' + str(cpu_count()), _critical=True )
            shprint(sh.make, '-j' + str(cpu_count()), 'install', _critical=True )


    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        info('Copying Qt5 java class to classes build dir')
        # TODO: neatly filter *.java and *.aidl
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.javaclass_dir)
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.aidl_dir)

recipe = Qt5Recipe()
