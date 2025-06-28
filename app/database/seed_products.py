"""
Database seeder script for products
"""
import json
import os
from pathlib import Path
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.database.database import SessionLocal, engine
from app.database import models
from app.database.models import Product


def load_mock_data(json_file_path: str) -> dict:
    """Load mock data from JSON file"""
    with open(json_file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def seed_products(db: Session, products_data: list) -> None:
    """Seed products table with mock data"""
    print("Starting to seed products...")

    # Check if products already exist
    existing_count = db.query(Product).count()
    if existing_count > 0:
        print(f"Products table already contains {existing_count} records.")
        response = input("Do you want to continue and add more products? (y/n): ")
        if response.lower() != 'y':
            print("Seeding cancelled.")
            return

    created_count = 0
    skipped_count = 0

    for product_data in products_data:
        # Check if product with same name already exists
        existing_product = db.query(Product).filter(
            Product.name == product_data["name"]
        ).first()

        if existing_product:
            print(f"Product '{product_data['name']}' already exists, skipping...")
            skipped_count += 1
            continue

        # Create new product
        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            image=product_data["image"]
        )

        db.add(product)
        created_count += 1
        print(f"Added product: {product_data['name']}")

    # Commit all changes
    try:
        db.commit()
        print(f"\n✅ Successfully seeded {created_count} products!")
        if skipped_count > 0:
            print(f"⚠️  Skipped {skipped_count} products (already exist)")
    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding products: {e}")
        raise


def main():
    """Main seeder function"""
    # Create tables if they don't exist
    models.Base.metadata.create_all(bind=engine)

    # Path to the JSON file (adjust as needed)
    json_file_path = Path(__file__).parent / "products.json"

    if not json_file_path.exists():
        print(f"❌ Mock data file not found: {json_file_path}")
        print("Please ensure 'products.json' is in the same directory as this script.")
        return

    # Load mock data
    try:
        mock_data = load_mock_data(json_file_path)
        products_data = mock_data.get("products", [])

        if not products_data:
            print("❌ No products data found in JSON file.")
            return

        print(f"📦 Found {len(products_data)} products in mock data file.")

    except Exception as e:
        print(f"❌ Error loading mock data: {e}")
        return

    # Create database session and seed products
    db = SessionLocal()
    try:
        seed_products(db, products_data)
    finally:
        db.close()


if __name__ == "__main__":
    main()


# Alternative function for use in FastAPI startup
async def seed_database_on_startup():
    """
    Alternative seeder function that can be called during FastAPI startup
    Add this to your main.py startup_event():

    # Add to your existing startup_event function:
    from app.database.seed_products import seed_database_on_startup
    await seed_database_on_startup()
    """
    from app.database.database import SessionLocal

    db = SessionLocal()
    try:
        # Only seed if database is empty
        if db.query(Product).count() == 0:
            json_file_path = Path(__file__).parent / "products.json"
            if json_file_path.exists():
                mock_data = load_mock_data(json_file_path)
                products_data = mock_data.get("products", [])
                seed_products(db, products_data)
                print("🚀 Database seeded on startup!")
    except Exception as e:
        print(f"❌ Error seeding database on startup: {e}")
    finally:
        db.close()


# CLI interface for more control
def cli_seed():
    """Command line interface for seeding with options"""
    import argparse

    parser = argparse.ArgumentParser(description="Seed products database")
    parser.add_argument("--force", action="store_true",
                       help="Force seed even if products exist")
    parser.add_argument("--clear", action="store_true",
                       help="Clear existing products before seeding")
    parser.add_argument("--file", type=str, default="products.json",
                       help="Path to JSON file with mock data")

    args = parser.parse_args()

    # Create tables
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if args.clear:
            print("🗑️  Clearing existing products...")
            db.query(Product).delete()
            db.commit()
            print("✅ Existing products cleared!")

        # Load and seed data
        json_file_path = Path(args.file)
        if not json_file_path.exists():
            print(f"❌ File not found: {json_file_path}")
            return

        mock_data = load_mock_data(json_file_path)
        products_data = mock_data.get("products", [])

        if args.force:
            # Force mode: don't check for existing products
            for product_data in products_data:
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    image=product_data["image"]
                )
                db.add(product)

            db.commit()
            print(f"✅ Force seeded {len(products_data)} products!")
        else:
            seed_products(db, products_data)

    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


# Usage examples:
# python seed_products.py                    # Normal seeding
# python seed_products.py --clear            # Clear and seed
# python seed_products.py --force            # Force seed without checks
# python seed_products.py --file custom.json # Use custom JSON file