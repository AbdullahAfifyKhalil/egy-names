"""faker-egy-names 0.1.1 — Python Faker showcase."""

from faker_egy_names import egyptian_faker

fake = egyptian_faker()

print("=" * 60)
print(" faker-egy-names 0.1.1 — Python")
print("=" * 60)

name = fake.egyptian_name(gender="female", religion="muslim", length=4, seed=1)
print("\n1. One coherent person — call egyptian_name() once:")
print(f"   {name.ar}")
print(f"   {name.en}")
print(f"   parts_ar: {name.parts_ar}")

print("\n2. Slot helpers (each call is a new chain):")
print(f"   full en: {fake.egyptian_full_name(seed=1)}")
print(f"   full ar: {fake.egyptian_full_name('ar', seed=1)}")
print(f"   person:  {fake.egyptian_person(gender='male', seed=2)}")
print(f"   father:  {fake.egyptian_father(seed=2)}")
print(f"   family:  {fake.egyptian_family(seed=2)}")

print("\nThere is no first_name / last_name mapping.")
