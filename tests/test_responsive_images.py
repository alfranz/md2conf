import unittest
from pathlib import Path

from md2conf.collection import ConfluencePageCollection
from md2conf.converter import ConfluenceDocument
from md2conf.domain import ConfluenceDocumentOptions
from md2conf.metadata import ConfluenceSiteMetadata
from tests.utility import TypedTestCase


class TestResponsiveImages(TypedTestCase):
    """Test cases for responsive image processing."""

    def setUp(self) -> None:
        self.maxDiff = None
        self.site_metadata = ConfluenceSiteMetadata("test.atlassian.net", "/wiki/", "TEST")
        self.page_metadata = ConfluencePageCollection()

    def test_responsive_images(self) -> None:
        """Test that images get responsive attributes."""
        test_dir = Path(__file__).parent
        source_file = test_dir / "source" / "responsive_test.md"
        
        options = ConfluenceDocumentOptions(image_width=700)
        _, doc = ConfluenceDocument.create(
            source_file,
            options,
            test_dir / "source",
            self.site_metadata,
            self.page_metadata,
        )
        
        xhtml = doc.xhtml()
        
        # Check that responsive attributes are present
        self.assertIn('width="700"', xhtml)
        self.assertIn('data-width="700"', xhtml)
        self.assertIn('style="max-width: 100%; height: auto;"', xhtml)
        
        # Large image should be scaled down with proportional height
        self.assertIn('data-height="467"', xhtml)  # 700 * 800 / 1200 = 467
        
        # Should have multiple responsive images
        self.assertTrue(xhtml.count('width="700"') >= 2)  # Multiple images with responsive width

    def test_custom_image_width(self) -> None:
        """Test custom image width setting."""
        test_dir = Path(__file__).parent
        source_file = test_dir / "source" / "responsive_test.md"
        
        options = ConfluenceDocumentOptions(image_width=500)
        _, doc = ConfluenceDocument.create(
            source_file,
            options,
            test_dir / "source",
            self.site_metadata,
            self.page_metadata,
        )
        
        xhtml = doc.xhtml()
        
        # Should use custom width for images
        self.assertIn('width="500"', xhtml)
        self.assertIn('data-width="500"', xhtml)
        self.assertIn('style="max-width: 100%; height: auto;"', xhtml)


if __name__ == "__main__":
    unittest.main()
