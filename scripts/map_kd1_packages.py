import os
import sys
import django
import argparse

# Setup Django
proj_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cbt_project.settings')
django.setup()

from collections import defaultdict
from ujian.models import Soal, PaketUjian, SubTest


def main(dry_run=True, per_subtest=10, max_packages=50):
    print('DRY RUN' if dry_run else 'APPLY MODE')

    # Determine subtest types present in KD1
    subtest_names = list(
        Soal.objects.filter(kategori='KD1', subtest__isnull=False)
        .values_list('subtest__nama', flat=True).distinct()
    )
    if not subtest_names:
        print('No subtest names found for KD1. Aborting.')
        return

    print('Detected subtest names:', subtest_names)

    # Pools: for each subtest name, get queryset of Soal with urutan null (unmapped)
    pools = {}
    for name in subtest_names:
        pools[name] = list(Soal.objects.filter(kategori='KD1', urutan__isnull=True, subtest__nama=name).order_by('id'))
        print(f"Pool for {name}: {len(pools[name])} questions")

    assignments = defaultdict(lambda: defaultdict(list))

    for i in range(1, max_packages + 1):
        for name in subtest_names:
            take = min(per_subtest, len(pools[name]))
            if take == 0:
                continue
            batch = pools[name][:take]
            pools[name] = pools[name][take:]
            assignments[i][name] = [q.id for q in batch]

    # Summary
    total_assigned = 0
    for pkg, groups in assignments.items():
        count_pkg = sum(len(v) for v in groups.values())
        if count_pkg:
            print(f"Package {pkg}: total {count_pkg}")
            for name, ids in groups.items():
                print(f"  {name}: {len(ids)}")
        total_assigned += count_pkg

    print('Total questions that would be assigned:', total_assigned)

    if dry_run:
        print('Dry run complete. No DB changes made.')
        return

    # Apply changes
    for pkg_num, groups in assignments.items():
        if not groups:
            continue
        paket_name = f"Konsep Dasar 1 {pkg_num}"
        paket, _ = PaketUjian.objects.get_or_create(nama=paket_name)
        print('Creating/using paket', paket_name)
        for name, ids in groups.items():
            subtest, _ = SubTest.objects.get_or_create(paket=paket, nama=name)
            qs = Soal.objects.filter(id__in=ids)
            for soal in qs:
                soal.subtest = subtest
                soal.urutan = pkg_num
                soal.save()

    print('Mapping applied.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--apply', action='store_true', help='Actually apply changes')
    parser.add_argument('--per-subtest', type=int, default=10, help='Questions per subtest per package')
    parser.add_argument('--max-packages', type=int, default=50, help='Number of packages to create')
    args = parser.parse_args()
    main(dry_run=not args.apply, per_subtest=args.per_subtest, max_packages=args.max_packages)
