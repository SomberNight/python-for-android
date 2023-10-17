from pythonforandroid.recipe import BootstrapNDKRecipe
from pythonforandroid.toolchain import Recipe, current_directory
from pythonforandroid.logger import info, debug, shprint
from os.path import join
import sh


class Qt6Recipe(BootstrapNDKRecipe):
    name = 'qt6'
    # version = '6.4.3'
    # url = 'https://download.qt.io/archive/qt/6.4/{version}/single/qt-everywhere-src-{version}.tar.xz'
    version = '6.5.3'
    url = 'https://download.qt.io/archive/qt/6.5/{version}/single/qt-everywhere-src-{version}.tar.xz'
    dir_name = 'qt6'

    built_libraries = {'dummy': '.'}

    depends = ['python3', 'hostqt6']
    conflicts = ['sdl2', 'genericndkbuild']
    # patches = ['add-way-to-disable-accessibility-env-var.patch']

    need_stl_shared = True

    # override as we can't statically define the libs due to arch in filename
    def get_libraries(self, arch_name, in_context=False):
        # TODO: don't hardcode, infer from build config
        self.built_libraries = {
            f'libQt6Core_{arch_name}.so': 'qtbase/lib',
            # f'libQt6Concurrent_{arch_name}.so': 'qtbase/lib',
            f'libQt6Gui_{arch_name}.so': 'qtbase/lib',
            f'libQt6Multimedia_{arch_name}.so': 'qtbase/lib',
            f'libQt6MultimediaQuick_{arch_name}.so': 'qtbase/lib',
            f'libQt6Network_{arch_name}.so': 'qtbase/lib',
            f'libQt6OpenGL_{arch_name}.so': 'qtbase/lib',
            f'libQt6Qml_{arch_name}.so': 'qtbase/lib',
            # f'libQt6QmlCore_{arch_name}.so': 'qtbase/lib',
            f'libQt6QmlModels_{arch_name}.so': 'qtbase/lib',
            f'libQt6QmlWorkerScript_{arch_name}.so': 'qtbase/lib',
            f'libQt6Quick_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickControls2_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickControls2Impl_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickDialogs2_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickDialogs2Utils_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickDialogs2QuickImpl_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickLayouts_{arch_name}.so': 'qtbase/lib',
            # f'libQt6QuickParticles_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickShapes_{arch_name}.so': 'qtbase/lib',
            f'libQt6QuickTemplates2_{arch_name}.so': 'qtbase/lib',
            # f'libQt6QuickTimeline_{arch_name}.so': 'qtbase/lib',
            f'libQt6ShaderTools_{arch_name}.so': 'qtbase/lib',
            f'libQt6Svg_{arch_name}.so': 'qtbase/lib',
            # f'libQt6Xml_{arch_name}.so': 'qtbase/lib',

            f'libplugins_platforms_qtforandroid_{arch_name}.so': 'qtbase/plugins/platforms',
            f'libplugins_imageformats_qjpeg_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qico_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qgif_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qtga_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qtiff_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qwebp_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qicns_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qwbmp_{arch_name}.so': 'qtbase/plugins/imageformats',
            f'libplugins_imageformats_qsvg_{arch_name}.so': 'qtbase/plugins/imageformats',

            f'libplugins_iconengines_qsvgicon_{arch_name}.so': 'qtbase/plugins/iconengines',
            f'libplugins_platforms_qtforandroid_{arch_name}.so': 'qtbase/plugins/platforms',
            f'libplugins_multimedia_androidmediaplugin_{arch_name}.so': 'qtbase/plugins/multimedia',
            f'libplugins_networkinformation_qandroidnetworkinformation_{arch_name}.so': 'qtbase/plugins/networkinformation',
            f'libplugins_tls_qopensslbackend_{arch_name}.so': 'qtbase/plugins/tls',
            f'libplugins_tls_qcertonlybackend_{arch_name}.so': 'qtbase/plugins/tls',

            f'libplugins_qmltooling_qmldbg_preview_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_native_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_debugger_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_local_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_messages_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_quickprofiler_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_nativedebugger_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_server_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_tcp_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_inspector_{arch_name}.so': 'qtbase/plugins/qmltooling',
            f'libplugins_qmltooling_qmldbg_profiler_{arch_name}.so': 'qtbase/plugins/qmltooling',

            f'libqml_QtQml_qmlmetaplugin_{arch_name}.so': 'qtbase/qml/QtQml',
            f'libqml_QtQml_WorkerScript_workerscriptplugin_{arch_name}.so': 'qtbase/qml/QtQml/WorkerScript',
            f'libqml_QtQml_Models_modelsplugin_{arch_name}.so': 'qtbase/qml/QtQml/Models',
            f'libqml_QtQuick_Window_quickwindowplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Window',
            f'libqml_QtQuick_Layouts_qquicklayoutsplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Layouts',
            f'libqml_QtQuick_Dialogs_qtquickdialogsplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Dialogs',
            f'libqml_QtQuick_Dialogs_quickimpl_qtquickdialogs2quickimplplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Dialogs/quickimpl',
            f'libqml_QtQuick_Shapes_qmlshapesplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Shapes',
            f'libqml_QtQuick_qtquick2plugin_{arch_name}.so': 'qtbase/qml/QtQuick',
            f'libqml_QtQuick_LocalStorage_qmllocalstorageplugin_{arch_name}.so': 'qtbase/qml/QtQuick/LocalStorage',
            f'libqml_QtQuick_Templates_qtquicktemplates2plugin_{arch_name}.so': 'qtbase/qml/QtQuick/Templates',
            f'libqml_QtQuick_Controls_qtquickcontrols2plugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls',
            f'libqml_QtQuick_Controls_impl_qtquickcontrols2implplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls/impl',
            f'libqml_QtQuick_Controls_Material_qtquickcontrols2materialstyleplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls/Material',
            f'libqml_QtQuick_Controls_Material_impl_qtquickcontrols2materialstyleimplplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls/Material/impl',
            f'libqml_QtQuick_Controls_Basic_qtquickcontrols2basicstyleplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls/Basic',
            f'libqml_QtQuick_Controls_Basic_impl_qtquickcontrols2basicstyleimplplugin_{arch_name}.so': 'qtbase/qml/QtQuick/Controls/Basic/impl',
            f'libqml_QtMultimedia_quickmultimediaplugin_{arch_name}.so': 'qtbase/qml/QtMultimedia',
        }

        return super().get_libraries(arch_name, in_context)

    def get_recipe_env(self, arch=None, with_flags_in_cc=True, with_python=True):
        env = super().get_recipe_env(
            arch=arch, with_flags_in_cc=with_flags_in_cc,
            with_python=with_python,
        )
        env['APP_ALLOW_MISSING_DEPS'] = 'true'
        build_dir = self.get_build_dir(arch.arch)
        env['QT_INSTALL_PATH'] = join(build_dir, 'install')
        env['QT_EXT_PATH'] = join(self.ctx.libs_dir, 'bin')
        return env

    def build_arch(self, arch):
        super().build_arch(arch)

        env = self.get_recipe_env(arch)
        with current_directory(self.get_jni_dir()):
            shprint(sh.Command(join(self.ctx.ndk_dir, "ndk-build")),
                    "V=1", _env=env, _critical=True)

        build_dir = self.get_build_dir(arch.arch)
        with current_directory(build_dir):
            info("compiling qt6 from sources")
            debug("environment: {}".format(env))

            ndk_sysroot = join(self.ctx.ndk_dir, 'sysroot')
            info("NDK sysroot: %s" % ndk_sysroot)
            info("libdir: %s" % join(build_dir, 'obj', 'local', arch.arch))

            configure = sh.Command('./configure')
            # options?
            shprint(configure, '--help', _env=env, _tail=50, _critical=True)
            shprint(configure, '-list-features', _env=env, _tail=50, _critical=True)

            configure = configure.bake('-opensource', '-confirm-license', '-disable-rpath')
            configure = configure.bake('-android-sdk', self.ctx.sdk_dir)
            configure = configure.bake('-android-ndk', self.ctx.ndk_dir)
            configure = configure.bake('-xplatform', 'android-clang')
            configure = configure.bake('-android-abis', arch.arch)
            configure = configure.bake('-prefix', join(build_dir, 'install'))
            configure = configure.bake('-extprefix', self.ctx.libs_dir)
            configure = configure.bake('-nomake', 'tests')
            configure = configure.bake('-nomake', 'examples')
            configure = configure.bake('-no-widgets')
            configure = configure.bake('-submodules', ','.join(
                ['qtbase', 'qtdeclarative', 'qtimageformats', 'qtmultimedia']))
            configure = configure.bake('-skip', ','.join(
                ['qtactiveqt']))

            # openssl
            openssl = Recipe.get_recipe('openssl', self.ctx)
            configure = configure.bake('-ssl', '-openssl-runtime')
            configure = configure.bake('OPENSSL_INCLUDE_DIR=' + join(openssl.get_build_dir(arch.arch), 'include'))
            configure = configure.bake('OPENSSL_LIBS=%s' % openssl.link_libs_flags().strip())

            # doesn't seem to have an effect:
            for exclude_feature in [
                    'quickcontrols2-fusion', 'quickcontrols2-imagine',
                    'quickcontrols2-universal', 'quickcontrols2-ios',
                    'quickcontrols2-macos', 'quickcontrols2-windows']:
                configure = configure.bake('-no-feature-%s' % exclude_feature)

            configure = configure.bake('--')

            from pythonforandroid.recipes.hostqt6 import HostQt6Recipe
            x = HostQt6Recipe()
            x.ctx = self.ctx
            env['LD_LIBRARY_PATH'] = join(x.get_install_dir(), 'lib')
            configure = configure.bake('-DQT_HOST_PATH=%s' % x.get_install_dir())

            shprint(configure, _tail=50, _env=env, _critical=True)

            shprint(sh.make, _env=env, _critical=True)
            shprint(sh.make, 'install', _env=env, _critical=True)

    def postbuild_arch(self, arch):
        super().postbuild_arch(arch)
        info('Copying Qt6 java class to classes build dir')
        # TODO: neatly filter *.java and *.aidl
        with current_directory(self.get_build_dir(arch.arch)):
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.javaclass_dir)
            shprint(sh.cp, '-a', join('qtbase', 'src', 'android', 'java', 'src', 'org'), self.ctx.aidl_dir)


recipe = Qt6Recipe()
