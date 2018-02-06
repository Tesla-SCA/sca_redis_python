import os.path
import sys
import time
import unittest

import redis

sys.path.append(os.path.join(os.path.dirname(__file__), '../'))
from redis_client import RedisClient


class TestRedisClient(unittest.TestCase):
    def setUp(self):
        self.sampe_key = 'sample_key'
        self.sample_value = 'sample_value'
        self.fetch_data_key = "cache_test_key"
        self.fetch_data_value = "cache missed value"
        self.short_data_key = "short_ttl_key"
        self.short_data_value = "short_ttl_value"
        self.test_redis_connection()
        self.test_redis_set_value()
        self.test_redis_get_value()
        self.test_fetch_data_with_custom_ttl()
        self.test_fetch_data_without_params()
        self.test_fetch_data_with_default_params()

    def tearDown(self):
        RedisClient().redis_client().delete(self.sampe_key, self.fetch_data_key, self.short_data_key)

    #### Redis connection ####
    def test_redis_connection(self):
        try:
            redis_client = RedisClient.redis_client()
            response = redis_client.client_list()
            self.assertNotEqual(response, None, "Redis connection error as response is None")
        except redis.ConnectionError:
            self.assertTrue(False)

    #### Redis set value ####
    def test_redis_set_value(self):
        redis_client = RedisClient.redis_client()
        redis_client.set(self.sampe_key, self.sample_value)
        self.assertEqual((redis_client.keys(pattern='sample_key*'))[0], self.sampe_key,
                         "Inserted key is not found. Set operation failed")

    #### Redis get value ####
    def test_redis_get_value(self):
        redis_client = RedisClient.redis_client()
        redis_client.set(self.sampe_key, self.sample_value)
        self.assertEqual(redis_client.get(self.sampe_key), self.sample_value,
                         "Inserted value is different from retrieved value. Get operation failed")

        #### Redis Fetch Data tests ####
        ## Redis fetch_data call without params ##

    def fetch_data_call_back(self):
        return self.fetch_data_value

    def short_data_call_back(self):
        return self.short_data_value

        ## Redis fetch_data call with 1 sec TTL ##

    def test_fetch_data_with_custom_ttl(self):
        ttl = 1
        fetch_data_result = RedisClient.fetch_data(self.short_data_key, self.short_data_call_back,
                                                   RedisClient.redis_params(ttl))
        # Add a delay of 3 sec for Redis to remove the key since TTL is set up to 1 sec.
        time.sleep(2)
        self.assertNotEqual(RedisClient.redis_client().get(self.short_data_key), self.short_data_value,
                            "Expected value should be different from retrieved value. fetch_data operation failed")

    def test_fetch_data_without_params(self):
        fetch_data_result = RedisClient.fetch_data(self.fetch_data_key, self.fetch_data_call_back)
        self.assertEqual(fetch_data_result, self.fetch_data_value,
                         "Expected value is different from retrieved value. fetch_data operation failed")

        ## Redis fetch_data call with default TTL ##

    def test_fetch_data_with_default_params(self):
        fetch_data_result = RedisClient.fetch_data(self.fetch_data_key, self.fetch_data_call_back,
                                                   RedisClient.redis_params())
        self.assertEqual(fetch_data_result, self.fetch_data_value,
                         "Expected value is different from retrieved value. fetch_data operation failed")

    #### Redis aws lambda request handler ####
    def aws_lambda_callback_method(self, event, context):
        return context.invoked_function_arn + str(event)

    def test_aws_lambda_request_handler(self):
        context = self.AwsContext()
        event = {'key1': 'value1', 'key2': 'value2'}
        fetch_data_result = RedisClient.aws_lambda_request_handler(event, context, self.aws_lambda_callback_method)
        print(fetch_data_result)
        self.assertEqual(fetch_data_result, self.aws_lambda_callback_method(event, context),
                         "Expected value is different from retrieved value. aws_lambda_request_handler does not work")

    #### Redis generic request handler ####
    def generic_query_callback_method(self, payload):
        pretend_response = "iQueried"
        return pretend_response + str(payload)

    def test_generic_request_handler(self):
        payload = {'address': 'pretend address', 'region': 'XY'}
        fetch_data_result = RedisClient.generic_request_handler(function_name='check_generic_handler', payload=payload,
                                                                callback_method=self.generic_query_callback_method)
        print(fetch_data_result)
        self.assertEqual(fetch_data_result, self.generic_query_callback_method(payload),
                         "Expected value is different from retrieved value. generic_request_handler does not work")

    class AwsContext:
        def __init__(self):
            self.invoked_function_arn = "FooBarBaz::baz:bar:foo"

