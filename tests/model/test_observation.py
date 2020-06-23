from datetime import datetime, timedelta
from unittest import TestCase, mock
from unittest.mock import MagicMock

import pytz

import ornitho
from ornitho import APIException, Detail, ModificationType, Observation

ornitho.consumer_key = "ORNITHO_CONSUMER_KEY"
ornitho.consumer_secret = "ORNITHO_CONSUMER_SECRET"
ornitho.user_email = "ORNITHO_USER_EMAIL"
ornitho.user_pw = "ORNITHO_USER_PW"
ornitho.api_base = "ORNITHO_API_BASE"


class TestObservation(TestCase):
    def setUp(self):
        self.observation_json = {
            "form": {"@id": "1", "full_form": "1"},
            "date": {"@notime": "1", "@offset": "3600", "@timestamp": "1573858800"},
            "species": {
                "@id": "94",
                "taxonomy": "1",
                "rarity": "common",
                "category": "B",
            },
            "place": {
                "@id": "779198",
                "id_universal": "28_43050307",
                "place_type": "place",
                "name": "Mohrbach-Aufstauung",
                "lat": "49.443127680501",
                "lon": "7.5751543757204",
                "loc_precision": "0",
            },
            "observers": [
                {
                    "@id": "10156",
                    "@uid": "53742",
                    "id_form": "1",
                    "traid": "10156",
                    "id_sighting": "43050307",
                    "id_universal": "28_43050307",
                    "guid": "2c789399-0939-41ea-ab12-01c00290e543",
                    "version": "0",
                    "timing": {
                        "@notime": "0",
                        "@offset": "3600",
                        "@timestamp": "1573899838",
                    },
                    "coord_lat": "49.443215",
                    "coord_lon": "7.574859",
                    "altitude": "233",
                    "precision": "precise",
                    "estimation_code": "EXACT_VALUE",
                    "count": "13",
                    "flight_number": "1",
                    "admin_hidden": "1",
                    "admin_hidden_type": "question",
                    "comment": "comment",
                    "hidden_comment": "hidden_comment",
                    "source": "WEB",
                    "insert_date": "1573995175",
                    "is_exported": "1",
                    "export_date": "1576641307",
                    "resting_habitat": "1_5",
                    "observation_detail": "4_2",
                    "details": [
                        {"count": "1", "sex": "U", "age": "PULL"},
                        {"count": "12", "sex": "M", "age": "AD"},
                    ],
                    "atlas_code": {"@id": "3_3", "#text": "A2"},
                }
            ],
        }
        self.observation = Observation.create_from(self.observation_json)

    def test_create_from(self):
        observation = Observation.create_from(self.observation_json)
        self.assertEqual(43050307, observation.id_)
        self.assertEqual(self.observation_json, observation._raw_data)

        # Test Exception
        self.assertRaises(
            APIException, lambda: Observation.create_from({"observers": ["1", "2"]}),
        )

    def test_id_observer(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["@id"]),
            self.observation.id_observer,
        )

    def test_traid(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["traid"]), self.observation.traid
        )

    def test_timing(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observation_json["observers"][0]["timing"]["@timestamp"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observation.timing,
        )

    def test_coord_lat(self):
        self.assertEqual(
            float(self.observation_json["observers"][0]["coord_lat"]),
            self.observation.coord_lat,
        )

    def test_coord_lon(self):
        self.assertEqual(
            float(self.observation_json["observers"][0]["coord_lon"]),
            self.observation.coord_lon,
        )

    def test_altitude(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["altitude"]),
            self.observation.altitude,
        )

    def test_id_form(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["id_form"]),
            self.observation.id_form,
        )

    def test_precision(self):
        self.assertEqual(
            self.observation_json["observers"][0]["precision"],
            self.observation.precision,
        )

    def test_estimation_code(self):
        self.assertEqual(
            self.observation_json["observers"][0]["estimation_code"],
            self.observation.estimation_code,
        )

    def test_id_species(self):
        self.assertEqual(
            int(self.observation_json["species"]["@id"]), self.observation.id_species
        )

    def test_count(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["count"]), self.observation.count
        )

    def test_flight_number(self):
        self.assertEqual(
            int(self.observation_json["observers"][0]["flight_number"]),
            self.observation.flight_number,
        )

    def test_admin_hidden(self):
        self.assertTrue(self.observation.admin_hidden,)

    def test_admin_hidden_type(self):
        self.assertEqual(
            self.observation_json["observers"][0]["admin_hidden_type"],
            self.observation.admin_hidden_type,
        )

    def test_source(self):
        self.assertEqual(
            self.observation_json["observers"][0]["source"], self.observation.source,
        )

    @mock.patch("ornitho.model.observation.Media")
    def test_medias(self, mock_media):
        mock_media.get.return_value = "Media retrieved"

        self.assertIsNone(self.observation.medias)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "medias": [{"@id": "111111",}, {"@id": "2222222",}],
                }
            ]
        }
        obs = Observation.create_from(obs_json)
        medias = obs.medias
        self.assertIsNotNone(medias)
        self.assertEqual(len(obs_json["observers"][0]["medias"]), len(medias))
        mock_media.get.assert_called_with(obs_json["observers"][0]["medias"][1]["@id"])

    def test_media_urls(self):
        self.assertIsNone(self.observation.media_urls)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "medias": [
                        {
                            "@id": "111111",
                            "path": "https://test.media/www.ornitho.de/1970-01",
                            "filename": "file1.jpg",
                        },
                        {
                            "@id": "2222222",
                            "path": "https://test.media/www.ornitho.de/1970-01",
                            "filename": "file2.jpg",
                        },
                    ],
                }
            ]
        }
        obs = Observation.create_from(obs_json)
        media_urls = obs.media_urls
        self.assertIsNotNone(media_urls)
        self.assertEqual(len(obs_json["observers"][0]["medias"]), len(media_urls))
        self.assertEqual(
            f"{obs_json['observers'][0]['medias'][0]['path']}/{obs_json['observers'][0]['medias'][0]['filename']}",
            media_urls[0],
        )
        self.assertEqual(
            f"{obs_json['observers'][0]['medias'][1]['path']}/{obs_json['observers'][0]['medias'][1]['filename']}",
            media_urls[1],
        )

    def test_comment(self):
        self.assertEqual(
            self.observation_json["observers"][0]["comment"], self.observation.comment,
        )

    def test_hidden_comment(self):
        self.assertEqual(
            self.observation_json["observers"][0]["hidden_comment"],
            self.observation.hidden_comment,
        )

    def test_hidden(self):
        self.assertFalse(self.observation.hidden)

    def test_id_atlas_code(self):
        self.assertEqual(
            self.observation_json["observers"][0]["atlas_code"]["@id"].split("_")[1],
            self.observation.id_atlas_code,
        )

    def test_atlas_code_text(self):
        self.assertEqual(
            self.observation_json["observers"][0]["atlas_code"]["#text"],
            self.observation.atlas_code_text,
        )

    def test_details(self):
        details = [Detail(1, "U", "PULL"), Detail(12, "M", "AD")]
        self.assertEqual(details, self.observation.details)

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "details": [
                        {
                            "count": "1",
                            "sex": {"@id": "U", "#text": "unbekannt"},
                            "age": {"@id": "PULL", "#text": "Pullus / nicht-flügge"},
                        },
                        {
                            "count": "12",
                            "sex": {"@id": "M", "#text": "Männchen"},
                            "age": {"@id": "AD", "#text": "adult"},
                        },
                    ],
                }
            ]
        }
        self.assertEqual(details, Observation.create_from(obs_json).details)

    def test_insert_date(self):
        self.assertEqual(
            datetime.fromtimestamp(
                int(self.observation_json["observers"][0]["insert_date"]),
                datetime.now().astimezone().tzinfo,
            ),
            self.observation.insert_date,
        )

    def test_update_date(self):
        self.assertEqual(None, self.observation.update_date)

    def test_id_place(self):
        self.assertEqual(
            int(self.observation_json["place"]["@id"]), self.observation.id_place
        )

    def test_id_resting_habitat(self):
        self.assertEqual(
            self.observation_json["observers"][0]["resting_habitat"],
            self.observation.id_resting_habitat,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "resting_habitat": {"@id": "1_5", "#text": "Grünland"},
                }
            ]
        }
        self.assertEqual(
            obs_json["observers"][0]["resting_habitat"]["@id"],
            Observation.create_from(obs_json).id_resting_habitat,
        )

        obs_json = {"observers": [{"id_sighting": "44874562",}]}
        self.assertIsNone(Observation.create_from(obs_json).id_resting_habitat)

    def test_id_observation_detail(self):
        self.assertEqual(
            self.observation_json["observers"][0]["observation_detail"],
            self.observation.id_observation_detail,
        )

        obs_json = {
            "observers": [
                {
                    "id_sighting": "44874562",
                    "observation_detail": {"@id": "4_2", "#text": "Nahrung suchend"},
                }
            ]
        }
        self.assertEqual(
            obs_json["observers"][0]["observation_detail"]["@id"],
            Observation.create_from(obs_json).id_observation_detail,
        )

        obs_json = {"observers": [{"id_sighting": "44874562",}]}
        self.assertIsNone(Observation.create_from(obs_json).id_observation_detail)

    def test_species(self):
        species = self.observation.species
        self.assertEqual(species._raw_data, self.observation_json["species"])

    def test_observer(self):
        observer = self.observation.observer
        self.assertEqual(observer._raw_data, self.observation_json["observers"][0])

    def test_place(self):
        place = self.observation.place
        self.assertEqual(place._raw_data, self.observation_json["place"])

    def test_form(self):
        form = self.observation.form
        self.assertEqual(form._raw_data, self.observation_json["form"])

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_resting_habitat(self, mock_field_option):
        mock_field_option.get.return_value = "Resting habitat retrieved"
        resting_habitat = self.observation.resting_habitat
        mock_field_option.get.assert_called_with(self.observation.id_resting_habitat)
        self.assertEqual(resting_habitat, "Resting habitat retrieved")

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_observation_detail(self, mock_field_option):
        mock_field_option.get.return_value = "Observation Detail retrieved"
        observation_detail = self.observation.observation_detail
        mock_field_option.get.assert_called_with(self.observation.id_observation_detail)
        self.assertEqual(observation_detail, "Observation Detail retrieved")

    @mock.patch("ornitho.model.observation.FieldOption")
    def test_atlas_code(self, mock_field_option):
        mock_field_option.get.return_value = "Atlas Code retrieved"
        atlas_code = self.observation.atlas_code
        mock_field_option.get.assert_called_with(f"3_{self.observation.id_atlas_code}")
        self.assertEqual(atlas_code, "Atlas Code retrieved")

    def test_by_observer(self):
        Observation.list = MagicMock(return_value=["obs", "pk"])
        Observation.by_observer(id_observer=1)
        Observation.list.assert_called_with(
            request_all=False, pagination_key=None, short_version=False, id_observer=1
        )

    def test_by_observer_all(self):
        Observation.list_all = MagicMock(return_value=["obs", "pk"])
        Observation.by_observer_all(id_observer=1)
        Observation.list_all.assert_called_with(id_observer=1, short_version=False)

    def test_diff(self):
        Observation.request = MagicMock(
            return_value=[
                {
                    "id_sighting": "1",
                    "id_universal": "1",
                    "modification_type": "updated",
                },
                {
                    "id_sighting": "2",
                    "id_universal": "2",
                    "modification_type": "deleted",
                },
            ]
        )

        # Case 1: without retrieving
        date = datetime.now() - timedelta(hours=1)
        observations = Observation.diff(
            date,
            modification_type=ModificationType.ALL,
            id_taxo_group=1,
            only_protocol="CBBM",
            only_form=True,
        )
        self.assertEqual(len(observations), 2)
        Observation.request.assert_called_with(
            method="get",
            url="observations/diff",
            params={
                "date": date.replace(microsecond=0).isoformat(),
                "modification_type": ModificationType.ALL.value,
                "id_taxo_group": 1,
                "only_protocol": "CBBM",
                "only_form": 1,
            },
        )

        # Case 2: with retrieving

        mock_protocol = MagicMock(spec=ornitho.Protocol)
        type(mock_protocol).name = mock.PropertyMock(return_value="CBBM-Mock")
        Observation.get = MagicMock(return_value=self.observation)
        date = datetime.now().astimezone(pytz.timezone("Asia/Tokyo")) - timedelta(
            hours=1
        )
        observations = Observation.diff(
            date, only_protocol=mock_protocol, retrieve_observations=True
        )
        self.assertEqual(len(observations), 2)
        self.assertEqual(observations[0], self.observation)
        Observation.request.assert_called_with(
            method="get",
            url="observations/diff",
            params={
                "date": date.replace(microsecond=0)
                .astimezone(datetime.now().astimezone().tzinfo)
                .replace(tzinfo=None)
                .isoformat(),
                "only_protocol": "CBBM-Mock",
            },
        )
