from pythonforandroid.toolchain import Bootstrap, current_directory, info, info_main, shprint
from pythonforandroid.util import ensure_dir
from os.path import join
import sh
import glob

class Qt5Bootstrap(Bootstrap):
    name = 'qt5'

    recipe_depends = list(
        set(Bootstrap.recipe_depends).union({'qt5'})
    )

    def distribute_aidl(self, aidl_dir, dest_dir="src"):
        '''Copy existing javaclasses from build dir to current dist dir.'''
        info('Copying aidl files')
        filenames = glob.glob(join(aidl_dir,'*'))
        if len(filenames) > 0:
            ensure_dir(dest_dir)
            shprint(sh.cp, '-a', *filenames, dest_dir)

    def assemble_distribution(self):
        info_main('# Creating Android project from build and {} bootstrap'.format(
            self.name))

        info('This currently just copies the build stuff straight from the build dir.')
        shprint(sh.rm, '-rf', self.dist_dir)
        shprint(sh.cp, '-r', self.build_dir, self.dist_dir)
        with current_directory(self.dist_dir):
            with open('local.properties', 'w') as fileh:
                fileh.write('sdk.dir={}'.format(self.ctx.sdk_dir))

        arch = self.ctx.archs[0]
        if len(self.ctx.archs) > 1:
            raise ValueError('built for more than one arch, but bootstrap cannot handle that yet')
        info('Bootstrap running with arch {}'.format(arch))

        with current_directory(self.dist_dir):
            info('Copying python distribution')

            self.distribute_libs(arch, [self.ctx.get_libs_dir(arch.arch)])
            self.distribute_aars(arch)
            self.distribute_javaclasses(self.ctx.javaclass_dir,
                                        dest_dir=join("src", "main", "java"))
            self.distribute_aidl(self.ctx.aidl_dir,
                                        dest_dir=join("src", "main", "aidl"))

            python_bundle_dir = join('_python_bundle', '_python_bundle')
            ensure_dir(python_bundle_dir)
            site_packages_dir = self.ctx.python_recipe.create_python_bundle(
                join(self.dist_dir, python_bundle_dir), arch)

            if 'sqlite3' not in self.ctx.recipe_build_order:
                with open('blacklist.txt', 'a') as fileh:
                    fileh.write('\nsqlite3/*\nlib-dynload/_sqlite3.so\n')

        if not self.ctx.with_debug_symbols:
            self.strip_libraries(arch)
        self.fry_eggs(site_packages_dir)
        super().assemble_distribution()


bootstrap = Qt5Bootstrap()
