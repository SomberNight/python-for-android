from pythonforandroid.toolchain import Bootstrap, current_directory, info, info_main, shprint
from pythonforandroid.util import ensure_dir
from os.path import join
import sh
import glob


class Qt6Bootstrap(Bootstrap):
    name = 'qt6'

    recipe_depends = list(
        set(Bootstrap.recipe_depends).union({'qt6'})
    )

    def distribute_aidl(self, aidl_dir, dest_dir="src"):
        '''Copy existing javaclasses from build dir to current dist dir.'''
        info('Copying aidl files')
        filenames = glob.glob(join(aidl_dir, '*'))
        if len(filenames) > 0:
            ensure_dir(dest_dir)
            shprint(sh.cp, '-a', *filenames, dest_dir)

    def assemble_distribution(self):
        info_main('# Creating Android project from build and {} bootstrap'.format(
            self.name))

        shprint(sh.rm, '-rf', self.dist_dir)
        shprint(sh.mkdir, '-p', self.dist_dir)

        file_include_patterns = [
            ('*', False),
            ('jni/*', False),
            ('jni/application/**', True),
            ('src/**', True),
            ('templates/**', True),
            ('gradle/**', True),
            ('**/*.so', True),
            ('**/qmldir', True),
        ]

        with current_directory(self.dist_dir):
            with open('bootstrap_distfiles.txt', 'w') as fileh:
                for pattern, recurse in file_include_patterns:
                    filenames = glob.glob(pattern, root_dir=self.build_dir, recursive=recurse)
                    for filename in filenames:
                        fileh.write(f'{filename}\n')
                    info(f'pattern {pattern}, recurse={recurse} yielded {len(filenames)} items')

            shprint(sh.rsync, '--files-from=bootstrap_distfiles.txt',
                self.build_dir, '.')

        with current_directory(self.dist_dir):
            with open('local.properties', 'w') as fileh:
                fileh.write('sdk.dir={}'.format(self.ctx.sdk_dir))

            info('Copying python distribution')

            # self.distribute_aars(arch)
            self.distribute_javaclasses(self.ctx.javaclass_dir,
                dest_dir=join("src", "main", "java"))
            self.distribute_aidl(self.ctx.aidl_dir,
                dest_dir=join("src", "main", "aidl"))

            for arch in self.ctx.archs:
                python_bundle_dir = join(f'_python_bundle__{arch.arch}', '_python_bundle')
                ensure_dir(python_bundle_dir)
                self.distribute_libs(arch, [self.ctx.get_libs_dir(arch.arch)])
                site_packages_dir = self.ctx.python_recipe.create_python_bundle(
                    join(self.dist_dir, python_bundle_dir), arch)
                if not self.ctx.with_debug_symbols:
                    self.strip_libraries(arch)
                self.fry_eggs(site_packages_dir)

            if 'sqlite3' not in self.ctx.recipe_build_order:
                with open('blacklist.txt', 'a') as fileh:
                    fileh.write('\nsqlite3/*\nlib-dynload/_sqlite3.so\n')

        super().assemble_distribution()


bootstrap = Qt6Bootstrap()
