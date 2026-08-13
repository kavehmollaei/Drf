# books/management/commands/generate_data.py

import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.db import transaction
from books.models import Publisher, Contributor, BookMetadata, Book   # adjust import

fake = Faker()

class Command(BaseCommand):
    help = 'Generate sample data for books, publishers, contributors, and metadata'

    # Define the counts as class constants (or use command-line arguments)
    NUM_PUBLISHERS = 10
    NUM_CONTRIBUTORS = 25
    NUM_BOOKS = 100
    NUM_METADATA = 200

    def add_arguments(self, parser):
        """Optional: Add command-line arguments to customize generation"""
        parser.add_argument(
            '--publishers',
            type=int,
            help='Number of publishers to create',
            default=self.NUM_PUBLISHERS
        )
        parser.add_argument(
            '--contributors',
            type=int,
            help='Number of contributors to create',
            default=self.NUM_CONTRIBUTORS
        )
        parser.add_argument(
            '--books',
            type=int,
            help='Number of books to create',
            default=self.NUM_BOOKS
        )
        parser.add_argument(
            '--metadata',
            type=int,
            help='Number of metadata objects to create',
            default=self.NUM_METADATA
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """
        This is the entry point that Django calls when you run:
        python manage.py generate_data
        """
        # Get counts from command-line arguments or use defaults
        num_publishers = options.get('publishers', self.NUM_PUBLISHERS)
        num_contributors = options.get('contributors', self.NUM_CONTRIBUTORS)
        num_books = options.get('books', self.NUM_BOOKS)
        num_metadata = options.get('metadata', self.NUM_METADATA)

        # Clear existing data (optional - uncomment if you want to start fresh)
        # Publisher.objects.all().delete()
        # Contributor.objects.all().delete()
        # BookMetadata.objects.all().delete()
        # Book.objects.all().delete()

        # 1. Create Publishers
        publishers = []
        for _ in range(num_publishers):
            publisher = Publisher.objects.create(
                name=fake.company(),
                email=fake.email()
            )
            publishers.append(publisher)

        # 2. Create Contributors
        contributors = []
        for _ in range(num_contributors):
            contributor = Contributor.objects.create(
                first_names=fake.first_name(),
                last_names=fake.last_name()
            )
            contributors.append(contributor)

        # 3. Create BookMetadata (pool)
        metadata_list = []
        for _ in range(num_metadata):
            metadata = BookMetadata.objects.create(
                summary=fake.paragraph(nb_sentences=3),
                page_count=random.randint(50, 500)
            )
            metadata_list.append(metadata)

        # 4. Create Books
        books_created = 0
        for _ in range(num_books):
            # Choose a random publisher (or None)
            publisher = random.choice(publishers + [None])

            # Choose a random metadata (or None)
            metadata = random.choice(metadata_list + [None])

            book = Book.objects.create(
                title=fake.sentence(nb_words=5).rstrip('.'),  # Remove trailing dot
                author=fake.name(),
                price=random.randint(500, 5000),
                publisher=publisher,
                metadata=metadata
            )
            books_created += 1

            # Add random contributors (many‑to‑many)
            num_contributors_for_book = random.randint(1, min(4, len(contributors)))
            selected_contributors = random.sample(contributors, num_contributors_for_book)
            book.contributors.add(*selected_contributors)

            # Remove used metadata to avoid OneToOne duplication
            if metadata and metadata in metadata_list:
                metadata_list.remove(metadata)

        # Use self.stdout for proper logging (instead of print)
        self.stdout.write(self.style.SUCCESS(
            f"✅ Successfully created:\n"
            f"   {num_publishers} publishers\n"
            f"   {num_contributors} contributors\n"
            f"   {books_created} books\n"
            f"   {num_metadata} metadata objects\n"
            f"   {num_metadata - len(metadata_list)} metadata objects assigned to books\n"
            f"   {len(metadata_list)} metadata objects remain unassigned"
        ))

        # Optional: Print some sample data
        self.stdout.write(self.style.WARNING("\nSample data created:"))
        sample_book = Book.objects.first()
        if sample_book:
            self.stdout.write(f"Sample Book: {sample_book.title}")
            self.stdout.write(f"  Author: {sample_book.author}")
            self.stdout.write(f"  Price: ${sample_book.price/100:.2f}")
            self.stdout.write(f"  Publisher: {sample_book.publisher}")
            self.stdout.write(f"  Contributors: {', '.join([str(c) for c in sample_book.contributors.all()[:3]])}")
            if sample_book.metadata:
                self.stdout.write(f"  Pages: {sample_book.metadata.page_count}")