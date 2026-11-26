import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

from handler import lambda_handler


class IncidentListTest(unittest.TestCase):
    @patch.dict(os.environ, {"INCIDENT_BUCKET": "test-bucket"})
    def test_reads_both_incidents_across_pages(self):
        fixtures = Path(__file__).resolve().parents[1] / "samples"
        files = sorted(fixtures.glob("*.json"))
        self.assertEqual(len(files), 2)
        s3 = Mock()
        paginator = s3.get_paginator.return_value
        paginator.paginate.return_value = [
            {"Contents": [{"Key": "incidents/" + f.name}]} for f in files
        ]
        s3.get_object.side_effect = lambda Bucket, Key: {
            "Body": io.BytesIO((fixtures / Path(Key).name).read_bytes())
        }
        event = {"rawPath": "/incidents", "requestContext": {"http": {"method": "GET"}}}
        response = lambda_handler(event, None, s3=s3)
        self.assertEqual(response["statusCode"], 200)
        ids = [item["id"] for item in json.loads(response["body"])["items"]]
        self.assertEqual(ids, [f.stem for f in files])
        paginator.paginate.assert_called_once_with(Bucket="test-bucket", Prefix="incidents/")
