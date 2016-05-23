SHARD_STATS_THIS_SECOND = {
    '356a9912480f4d8a8ac032eb89d1ce81': {
        'per_node_stats': {
            'iad1clus01br0vz291.iad1.devtools:33291': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 22,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 10.406852248394005,
                    'flushes': 467,
                    'last_finished': '1463693925',
                    'last_ms': 2,
                    'total_ms': 4860
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 2,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 16531986,
                    'totalTime': 80925019000
                },
                'indexCounters': {
                    'accesses': 112950,
                    'hits': 112950,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 4552698,
                            'W': 209258496
                        },
                        'timeLockedMicros': {
                            'R': 3143081,
                            'W': 16531986
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 3320563,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 140967898,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 266235397,
                            'w': 77239
                        },
                        'timeLockedMicros': {
                            'r': 471329925,
                            'w': 527767
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 81047900,
                            'w': 472054
                        },
                        'timeLockedMicros': {
                            'r': 133109305,
                            'w': 3166381
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 2
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 18768,
                        'returned': 50276,
                        'updated': 71
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 68,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 156,
                        'scannedObjects': 156
                    },
                    'record': {
                        'moves': 0
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'ops': 0
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 67680,
                            'getmores': {
                                'num': 1881,
                                'totalMillis': 62578598
                            },
                            'ops': 0,
                            'readersCreated': 21
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 0,
                                'totalMillis': 0
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 18998,
                                'scanned': 35481
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 462
                    }
                },
                'network': {
                    'bytesIn': 18697388,
                    'bytesOut': 43213535,
                    'numRequests': 81444
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 59669,
                    'delete': 0,
                    'getmore': 20661,
                    'insert': 18768,
                    'query': 1419,
                    'update': 71
                },
                'opcountersRepl': {
                    'command': 0,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 0,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 1,
                    'admin': {
                        'accessesNotInMemory': 1,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 80925.0,
                'uptimeMillis': 80925018,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz609.iad1.devtools:33609': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 14,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 3.147751605995717,
                    'flushes': 467,
                    'last_finished': '1463693925',
                    'last_ms': 1,
                    'total_ms': 1470
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 0,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 6586221,
                    'totalTime': 80924331000
                },
                'indexCounters': {
                    'accesses': 249870,
                    'hits': 249870,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 742355,
                            'W': 47333200
                        },
                        'timeLockedMicros': {
                            'R': 3198686,
                            'W': 6586221,
                            'r': 0,
                            'w': 62599
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 1749462,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 47266528,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 27444112,
                            'w': 214513
                        },
                        'timeLockedMicros': {
                            'r': 78907267,
                            'w': 2727173
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 6979580,
                            'w': 47152
                        },
                        'timeLockedMicros': {
                            'r': 48361458,
                            'w': 1564500
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 0
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 0,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 95,
                        'scannedObjects': 95
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 6520,
                                'totalMillis': 1711
                            },
                            'ops': 25095
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 10248643,
                            'getmores': {
                                'num': 12143,
                                'totalMillis': 80670721
                            },
                            'ops': 25094,
                            'readersCreated': 123
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 50182,
                                'totalMillis': 90
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 19001,
                                'scanned': 35484
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 465
                    }
                },
                'network': {
                    'bytesIn': 5702678,
                    'bytesOut': 10712247,
                    'numRequests': 36058
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 36060,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 1,
                    'query': 1354,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 1,
                    'delete': 6325,
                    'getmore': 0,
                    'insert': 18769,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 17,
                    'admin': {
                        'accessesNotInMemory': 1,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 16,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 80924.0,
                'uptimeMillis': 80924331,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz976.iad1.devtools:32976': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 10,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 5.802997858672377,
                    'flushes': 467,
                    'last_finished': '1463693927',
                    'last_ms': 3,
                    'total_ms': 2710
                },
                'cursors': {
                    'clientCursors_size': 2,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 13,
                    'totalNoTimeout': 0,
                    'totalOpen': 2
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 40699314,
                    'totalTime': 80923147000
                },
                'indexCounters': {
                    'accesses': 249868,
                    'hits': 249868,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 22768964,
                            'W': 195087350
                        },
                        'timeLockedMicros': {
                            'R': 2730117,
                            'W': 40699314,
                            'r': 0,
                            'w': 69986
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 7358482,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 60097742,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 741804734,
                            'w': 234840
                        },
                        'timeLockedMicros': {
                            'r': 660609774,
                            'w': 2917948
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 7946247,
                            'w': 55413
                        },
                        'timeLockedMicros': {
                            'r': 118949099,
                            'w': 1648422
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 2
                        },
                        'timedOut': 13
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 32,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 25225,
                        'scannedObjects': 25225
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 6631,
                                'totalMillis': 1939
                            },
                            'ops': 25095
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 10257699,
                            'getmores': {
                                'num': 10399,
                                'totalMillis': 18140466
                            },
                            'ops': 25094,
                            'readersCreated': 20
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 50182,
                                'totalMillis': 138
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 19001,
                                'scanned': 35484
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 463
                    }
                },
                'network': {
                    'bytesIn': 6065756,
                    'bytesOut': 15972730,
                    'numRequests': 42884
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 39095,
                    'delete': 0,
                    'getmore': 3764,
                    'insert': 1,
                    'query': 1379,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 1,
                    'delete': 6325,
                    'getmore': 0,
                    'insert': 18769,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 10,
                    'admin': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 10,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 80923.0,
                'uptimeMillis': 80923147,
                'version': '2.6.11',
                'writeBacksQueued': False
            }
        },
        'replication_lag': 0.0,
        'shard_stats': {
            'asserts': {
                'msg': 0,
                'regular': 0,
                'rollovers': 0,
                'user': 10,
                'warning': 0
            },
            'backgroundFlushing': {
                'average_ms': 5.802997858672377,
                'flushes': 467,
                'last_finished': '1463693927',
                'last_ms': 3,
                'total_ms': 2710
            },
            'connections': {
                'available': 838845,
                'current': 15,
                'totalCreated': 2250
            },
            'cursors': {
                'clientCursors_size': 2,
                'note': 'deprecated, use server status metrics',
                'pinned': 0,
                'timedOut': 13,
                'totalNoTimeout': 0,
                'totalOpen': 2
            },
            'globalLock': {
                'activeClients': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'currentQueue': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'lockTime': 40699314,
                'totalTime': 80923115000
            },
            'indexCounters': {
                'accesses': 249866,
                'hits': 249866,
                'missRatio': 0.0,
                'misses': 0,
                'resets': 0
            },
            'locks': {
                '.': {
                    'timeAcquiringMicros': {
                        'R': 22768963,
                        'W': 195087350
                    },
                    'timeLockedMicros': {
                        'R': 2730115,
                        'W': 40699314,
                        'r': 0,
                        'w': 69986
                    }
                },
                'admin': {
                    'timeAcquiringMicros': {
                        'r': 7358478,
                        'w': 0
                    },
                    'timeLockedMicros': {
                        'r': 60097234,
                        'w': 0
                    }
                },
                'local': {
                    'timeAcquiringMicros': {
                        'r': 741804732,
                        'w': 234840
                    },
                    'timeLockedMicros': {
                        'r': 660609768,
                        'w': 2917948
                    }
                },
                'main': {
                    'timeAcquiringMicros': {
                        'r': 7946245,
                        'w': 55413
                    },
                    'timeLockedMicros': {
                        'r': 118949097,
                        'w': 1648422
                    }
                }
            },
            'metrics': {
                'cursor': {
                    'open': {
                        'noTimeout': 0,
                        'pinned': 0,
                        'total': 2
                    },
                    'timedOut': 13
                },
                'document': {
                    'deleted': 0,
                    'inserted': 1,
                    'returned': 32,
                    'updated': 0
                },
                'getLastError': {
                    'wtime': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'wtimeouts': 0
                },
                'operation': {
                    'fastmod': 0,
                    'idhack': 0,
                    'scanAndOrder': 0
                },
                'queryExecutor': {
                    'scanned': 25225,
                    'scannedObjects': 25225
                },
                'record': {
                    'moves': 1
                },
                'repl': {
                    'apply': {
                        'batches': {
                            'num': 6631,
                            'totalMillis': 1939
                        },
                        'ops': 25095
                    },
                    'buffer': {
                        'count': 0,
                        'maxSizeBytes': 268435456,
                        'sizeBytes': 0
                    },
                    'network': {
                        'bytes': 10257699,
                        'getmores': {
                            'num': 10399,
                            'totalMillis': 18140466
                        },
                        'ops': 25094,
                        'readersCreated': 20
                    },
                    'preload': {
                        'docs': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'indexes': {
                            'num': 50182,
                            'totalMillis': 138
                        }
                    }
                },
                'storage': {
                    'freelist': {
                        'search': {
                            'bucketExhausted': 0,
                            'requests': 19001,
                            'scanned': 35484
                        }
                    }
                },
                'ttl': {
                    'deletedDocuments': 0,
                    'passes': 463
                }
            },
            'network': {
                'bytesIn': 6065044,
                'bytesOut': 15963838,
                'numRequests': 42875
            },
            'ok': 1.0,
            'opcounters': {
                'command': 39086,
                'delete': 0,
                'getmore': 3764,
                'insert': 1,
                'query': 1379,
                'update': 0
            },
            'opcountersRepl': {
                'command': 1,
                'delete': 6325,
                'getmore': 0,
                'insert': 18769,
                'query': 0,
                'update': 0
            },
            'pid': 1,
            'recordStats': {
                'accessesNotInMemory': 10,
                'admin': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'local': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'main': {
                    'accessesNotInMemory': 10,
                    'pageFaultExceptionsThrown': 0
                },
                'pageFaultExceptionsThrown': 0
            },
            'uptime': 80923.0,
            'uptimeMillis': 80923114,
            'version': '2.6.11',
            'writeBacksQueued': False
        }
    },
    '4d558d4e694249cba6352252dbc7e443': {
        'per_node_stats': {
            'iad1clus01br0vz544.iad1.devtools:33544': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 12,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 12.561712846347607,
                    'flushes': 397,
                    'last_finished': '1463693940',
                    'last_ms': 1,
                    'total_ms': 4987
                },
                'cursors': {
                    'clientCursors_size': 2,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 13,
                    'totalNoTimeout': 0,
                    'totalOpen': 2
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 21657548,
                    'totalTime': 76712245000
                },
                'indexCounters': {
                    'accesses': 75516,
                    'hits': 75516,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 1008481,
                            'W': 268090464
                        },
                        'timeLockedMicros': {
                            'R': 2761304,
                            'W': 21657548
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 17697951,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 140867662,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 558667409,
                            'w': 52398
                        },
                        'timeLockedMicros': {
                            'r': 769874999,
                            'w': 281889
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 53752472,
                            'w': 54690
                        },
                        'timeLockedMicros': {
                            'r': 138463415,
                            'w': 1729064
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 2
                        },
                        'timedOut': 13
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 6402,
                        'returned': 25525,
                        'updated': 63
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 60,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 126,
                        'scannedObjects': 126
                    },
                    'record': {
                        'moves': 0
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'ops': 0
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 0,
                            'getmores': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'ops': 0,
                            'readersCreated': 13
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 0,
                                'totalMillis': 0
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 12919,
                                'scanned': 25826
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 391
                    }
                },
                'network': {
                    'bytesIn': 12008669,
                    'bytesOut': 34980631,
                    'numRequests': 74444
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 51321,
                    'delete': 0,
                    'getmore': 22558,
                    'insert': 6415,
                    'query': 1236,
                    'update': 63
                },
                'opcountersRepl': {
                    'command': 0,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 0,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 1,
                    'admin': {
                        'accessesNotInMemory': 1,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 76712.0,
                'uptimeMillis': 76712244,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz588.iad1.devtools:33588': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 15,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 6.740554156171284,
                    'flushes': 397,
                    'last_finished': '1463693940',
                    'last_ms': 1,
                    'total_ms': 2676
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 0,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 11926659,
                    'totalTime': 76711072000
                },
                'indexCounters': {
                    'accesses': 126183,
                    'hits': 126183,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 329100,
                            'W': 61068466
                        },
                        'timeLockedMicros': {
                            'R': 2387963,
                            'W': 11926659,
                            'r': 0,
                            'w': 81525
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 1162476,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 63024216,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 46248978,
                            'w': 153245
                        },
                        'timeLockedMicros': {
                            'r': 104986479,
                            'w': 1868106
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 542944,
                            'w': 24451
                        },
                        'timeLockedMicros': {
                            'r': 43953198,
                            'w': 716802
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 0
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 1,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 142,
                        'scannedObjects': 142
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 6626,
                                'totalMillis': 416
                            },
                            'ops': 12729
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 6739916,
                            'getmores': {
                                'num': 11229,
                                'totalMillis': 76436163
                            },
                            'ops': 12728,
                            'readersCreated': 60
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 25450,
                                'totalMillis': 12
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 12922,
                                'scanned': 25829
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 394
                    }
                },
                'network': {
                    'bytesIn': 4731986,
                    'bytesOut': 8183226,
                    'numRequests': 28823
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 28827,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 1,
                    'query': 1190,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 1,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 12728,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 2,
                    'admin': {
                        'accessesNotInMemory': 2,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 76711.0,
                'uptimeMillis': 76711072,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz770.iad1.devtools:32770': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 12,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 5.1158690176322414,
                    'flushes': 397,
                    'last_finished': '1463693941',
                    'last_ms': 2,
                    'total_ms': 2031
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 0,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 7328163,
                    'totalTime': 76710386000
                },
                'indexCounters': {
                    'accesses': 126182,
                    'hits': 126182,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 424716,
                            'W': 36430185
                        },
                        'timeLockedMicros': {
                            'R': 2204416,
                            'W': 7328163,
                            'r': 0,
                            'w': 71119
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 583517,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 65872773,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 17649009,
                            'w': 89848
                        },
                        'timeLockedMicros': {
                            'r': 57464178,
                            'w': 1256493
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 335687,
                            'w': 27642
                        },
                        'timeLockedMicros': {
                            'r': 27675080,
                            'w': 631291
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 0
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 0,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 133,
                        'scannedObjects': 133
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 6727,
                                'totalMillis': 287
                            },
                            'ops': 12729
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 6743480,
                            'getmores': {
                                'num': 11327,
                                'totalMillis': 76454737
                            },
                            'ops': 12728,
                            'readersCreated': 45
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 25450,
                                'totalMillis': 0
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 12922,
                                'scanned': 25829
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 395
                    }
                },
                'network': {
                    'bytesIn': 4737386,
                    'bytesOut': 8188768,
                    'numRequests': 28853
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 28856,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 1,
                    'query': 1191,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 1,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 12728,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 3,
                    'admin': {
                        'accessesNotInMemory': 3,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 76710.0,
                'uptimeMillis': 76710386,
                'version': '2.6.11',
                'writeBacksQueued': False
            }
        },
        'replication_lag': 0.0,
        'shard_stats': {
            'asserts': {
                'msg': 0,
                'regular': 0,
                'rollovers': 0,
                'user': 12,
                'warning': 0
            },
            'backgroundFlushing': {
                'average_ms': 12.561712846347607,
                'flushes': 397,
                'last_finished': '1463693940',
                'last_ms': 1,
                'total_ms': 4987
            },
            'connections': {
                'available': 838845,
                'current': 15,
                'totalCreated': 2013
            },
            'cursors': {
                'clientCursors_size': 2,
                'note': 'deprecated, use server status metrics',
                'pinned': 0,
                'timedOut': 13,
                'totalNoTimeout': 0,
                'totalOpen': 2
            },
            'globalLock': {
                'activeClients': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'currentQueue': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'lockTime': 21657548,
                'totalTime': 76712209000
            },
            'indexCounters': {
                'accesses': 75514,
                'hits': 75514,
                'missRatio': 0.0,
                'misses': 0,
                'resets': 0
            },
            'locks': {
                '.': {
                    'timeAcquiringMicros': {
                        'R': 1008481,
                        'W': 268090464
                    },
                    'timeLockedMicros': {
                        'R': 2761304,
                        'W': 21657548
                    }
                },
                'admin': {
                    'timeAcquiringMicros': {
                        'r': 17697946,
                        'w': 0
                    },
                    'timeLockedMicros': {
                        'r': 140867461,
                        'w': 0
                    }
                },
                'local': {
                    'timeAcquiringMicros': {
                        'r': 558667407,
                        'w': 52398
                    },
                    'timeLockedMicros': {
                        'r': 769874990,
                        'w': 281889
                    }
                },
                'main': {
                    'timeAcquiringMicros': {
                        'r': 53752470,
                        'w': 54690
                    },
                    'timeLockedMicros': {
                        'r': 138463412,
                        'w': 1729064
                    }
                }
            },
            'metrics': {
                'cursor': {
                    'open': {
                        'noTimeout': 0,
                        'pinned': 0,
                        'total': 2
                    },
                    'timedOut': 13
                },
                'document': {
                    'deleted': 0,
                    'inserted': 6402,
                    'returned': 25525,
                    'updated': 63
                },
                'getLastError': {
                    'wtime': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'wtimeouts': 0
                },
                'operation': {
                    'fastmod': 60,
                    'idhack': 0,
                    'scanAndOrder': 0
                },
                'queryExecutor': {
                    'scanned': 126,
                    'scannedObjects': 126
                },
                'record': {
                    'moves': 0
                },
                'repl': {
                    'apply': {
                        'batches': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'ops': 0
                    },
                    'buffer': {
                        'count': 0,
                        'maxSizeBytes': 268435456,
                        'sizeBytes': 0
                    },
                    'network': {
                        'bytes': 0,
                        'getmores': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'ops': 0,
                        'readersCreated': 13
                    },
                    'preload': {
                        'docs': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'indexes': {
                            'num': 0,
                            'totalMillis': 0
                        }
                    }
                },
                'storage': {
                    'freelist': {
                        'search': {
                            'bucketExhausted': 0,
                            'requests': 12919,
                            'scanned': 25826
                        }
                    }
                },
                'ttl': {
                    'deletedDocuments': 0,
                    'passes': 391
                }
            },
            'network': {
                'bytesIn': 12007957,
                'bytesOut': 34971783,
                'numRequests': 74435
            },
            'ok': 1.0,
            'opcounters': {
                'command': 51312,
                'delete': 0,
                'getmore': 22558,
                'insert': 6415,
                'query': 1236,
                'update': 63
            },
            'opcountersRepl': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'pid': 1,
            'recordStats': {
                'accessesNotInMemory': 1,
                'admin': {
                    'accessesNotInMemory': 1,
                    'pageFaultExceptionsThrown': 0
                },
                'local': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'main': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'pageFaultExceptionsThrown': 0
            },
            'uptime': 76712.0,
            'uptimeMillis': 76712207,
            'version': '2.6.11',
            'writeBacksQueued': False
        }
    },
    'e4f8cc3415954cb98852c98fd659ce95': {
        'per_node_stats': {
            'iad1clus01br0vz369.iad1.devtools:33369': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 14,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 8.092050209205022,
                    'flushes': 717,
                    'last_finished': '1463693902',
                    'last_ms': 2,
                    'total_ms': 5802
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 10,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 24325750,
                    'totalTime': 132517359000
                },
                'indexCounters': {
                    'accesses': 211330,
                    'hits': 211330,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 6941683,
                            'W': 324581223
                        },
                        'timeLockedMicros': {
                            'R': 2675718,
                            'W': 24325750
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 7823904,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 196625714,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 645944416,
                            'w': 331299
                        },
                        'timeLockedMicros': {
                            'r': 1203382974,
                            'w': 801500
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 2590777,
                            'w': 37008
                        },
                        'timeLockedMicros': {
                            'r': 123701170,
                            'w': 3626424
                        }
                    },
                    'zips': {
                        'timeAcquiringMicros': {
                            'r': 10,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 105,
                            'w': 0
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 10
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 80266,
                        'returned': 160990,
                        'updated': 85
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 82,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 80469,
                        'scannedObjects': 80469
                    },
                    'record': {
                        'moves': 0
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'ops': 0
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 68256,
                            'getmores': {
                                'num': 1896,
                                'totalMillis': 62555584
                            },
                            'ops': 0,
                            'readersCreated': 19
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 0,
                                'totalMillis': 0
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 80785,
                                'scanned': 161553
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 711
                    }
                },
                'network': {
                    'bytesIn': 38455366,
                    'bytesOut': 83904651,
                    'numRequests': 99608
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 77125,
                    'delete': 0,
                    'getmore': 20234,
                    'insert': 80266,
                    'query': 2267,
                    'update': 85
                },
                'opcountersRepl': {
                    'command': 0,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 0,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 2,
                    'admin': {
                        'accessesNotInMemory': 2,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 132518.0,
                'uptimeMillis': 132517359,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz505.iad1.devtools:33505': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 13,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 5.062761506276151,
                    'flushes': 717,
                    'last_finished': '1463693902',
                    'last_ms': 2,
                    'total_ms': 3630
                },
                'cursors': {
                    'clientCursors_size': 2,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 10,
                    'totalNoTimeout': 0,
                    'totalOpen': 2
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 17428935,
                    'totalTime': 132516500000
                },
                'indexCounters': {
                    'accesses': 581087,
                    'hits': 581084,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 5968032,
                            'W': 85482840
                        },
                        'timeLockedMicros': {
                            'R': 3735896,
                            'W': 17428935,
                            'r': 0,
                            'w': 567667
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 1274132,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 49307019,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 186079132,
                            'w': 150543
                        },
                        'timeLockedMicros': {
                            'r': 289353037,
                            'w': 3202621
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 1441132,
                            'w': 112204
                        },
                        'timeLockedMicros': {
                            'r': 44431524,
                            'w': 2502893
                        }
                    },
                    'zips': {
                        'timeAcquiringMicros': {
                            'r': 5,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 839,
                            'w': 0
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 2
                        },
                        'timedOut': 10
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 28,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 159,
                        'scannedObjects': 159
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 3106,
                                'totalMillis': 2754
                            },
                            'ops': 80272
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 29979685,
                            'getmores': {
                                'num': 10088,
                                'totalMillis': 69667749
                            },
                            'ops': 80271,
                            'readersCreated': 43
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 105816,
                                'totalMillis': 198
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 80788,
                                'scanned': 161556
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 715
                    }
                },
                'network': {
                    'bytesIn': 8874770,
                    'bytesOut': 19304555,
                    'numRequests': 57495
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 53672,
                    'delete': 0,
                    'getmore': 3800,
                    'insert': 1,
                    'query': 2177,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 6,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 80266,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 3,
                    'admin': {
                        'accessesNotInMemory': 3,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 132517.0,
                'uptimeMillis': 132516500,
                'version': '2.6.11',
                'writeBacksQueued': False
            },
            'iad1clus01br0vz851.iad1.devtools:32851': {
                'asserts': {
                    'msg': 0,
                    'regular': 0,
                    'rollovers': 0,
                    'user': 13,
                    'warning': 0
                },
                'backgroundFlushing': {
                    'average_ms': 4.398884239888424,
                    'flushes': 717,
                    'last_finished': '1463693902',
                    'last_ms': 4,
                    'total_ms': 3154
                },
                'cursors': {
                    'clientCursors_size': 0,
                    'note': 'deprecated, use server status metrics',
                    'pinned': 0,
                    'timedOut': 0,
                    'totalNoTimeout': 0,
                    'totalOpen': 0
                },
                'globalLock': {
                    'activeClients': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'currentQueue': {
                        'readers': 0,
                        'total': 0,
                        'writers': 0
                    },
                    'lockTime': 7677770,
                    'totalTime': 132515684000
                },
                'indexCounters': {
                    'accesses': 580973,
                    'hits': 580970,
                    'missRatio': 0.0,
                    'misses': 0,
                    'resets': 0
                },
                'locks': {
                    '.': {
                        'timeAcquiringMicros': {
                            'R': 703704,
                            'W': 33964125
                        },
                        'timeLockedMicros': {
                            'R': 4333407,
                            'W': 7677770,
                            'r': 0,
                            'w': 58797
                        }
                    },
                    'admin': {
                        'timeAcquiringMicros': {
                            'r': 5105161,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 37477437,
                            'w': 0
                        }
                    },
                    'local': {
                        'timeAcquiringMicros': {
                            'r': 17643254,
                            'w': 265568
                        },
                        'timeLockedMicros': {
                            'r': 50828100,
                            'w': 3216722
                        }
                    },
                    'main': {
                        'timeAcquiringMicros': {
                            'r': 379938,
                            'w': 85443
                        },
                        'timeLockedMicros': {
                            'r': 60111144,
                            'w': 2515116
                        }
                    },
                    'zips': {
                        'timeAcquiringMicros': {
                            'r': 9,
                            'w': 0
                        },
                        'timeLockedMicros': {
                            'r': 416,
                            'w': 0
                        }
                    }
                },
                'metrics': {
                    'cursor': {
                        'open': {
                            'noTimeout': 0,
                            'pinned': 0,
                            'total': 0
                        },
                        'timedOut': 0
                    },
                    'document': {
                        'deleted': 0,
                        'inserted': 1,
                        'returned': 84,
                        'updated': 0
                    },
                    'getLastError': {
                        'wtime': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'wtimeouts': 0
                    },
                    'operation': {
                        'fastmod': 0,
                        'idhack': 0,
                        'scanAndOrder': 0
                    },
                    'queryExecutor': {
                        'scanned': 171,
                        'scannedObjects': 171
                    },
                    'record': {
                        'moves': 1
                    },
                    'repl': {
                        'apply': {
                            'batches': {
                                'num': 2878,
                                'totalMillis': 2803
                            },
                            'ops': 80272
                        },
                        'buffer': {
                            'count': 0,
                            'maxSizeBytes': 268435456,
                            'sizeBytes': 0
                        },
                        'network': {
                            'bytes': 30211152,
                            'getmores': {
                                'num': 12048,
                                'totalMillis': 132368075
                            },
                            'ops': 80271,
                            'readersCreated': 38
                        },
                        'preload': {
                            'docs': {
                                'num': 0,
                                'totalMillis': 0
                            },
                            'indexes': {
                                'num': 105816,
                                'totalMillis': 135
                            }
                        }
                    },
                    'storage': {
                        'freelist': {
                            'search': {
                                'bucketExhausted': 0,
                                'requests': 80788,
                                'scanned': 161556
                            }
                        }
                    },
                    'ttl': {
                        'deletedDocuments': 0,
                        'passes': 716
                    }
                },
                'network': {
                    'bytesIn': 8505114,
                    'bytesOut': 13868342,
                    'numRequests': 50616
                },
                'ok': 1.0,
                'opcounters': {
                    'command': 50605,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 1,
                    'query': 2165,
                    'update': 0
                },
                'opcountersRepl': {
                    'command': 6,
                    'delete': 0,
                    'getmore': 0,
                    'insert': 80266,
                    'query': 0,
                    'update': 0
                },
                'pid': 1,
                'recordStats': {
                    'accessesNotInMemory': 1,
                    'admin': {
                        'accessesNotInMemory': 1,
                        'pageFaultExceptionsThrown': 0
                    },
                    'local': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'main': {
                        'accessesNotInMemory': 0,
                        'pageFaultExceptionsThrown': 0
                    },
                    'pageFaultExceptionsThrown': 0
                },
                'uptime': 132516.0,
                'uptimeMillis': 132515684,
                'version': '2.6.11',
                'writeBacksQueued': False
            }
        },
        'replication_lag': 0.0,
        'shard_stats': {
            'asserts': {
                'msg': 0,
                'regular': 0,
                'rollovers': 0,
                'user': 13,
                'warning': 0
            },
            'backgroundFlushing': {
                'average_ms': 5.062761506276151,
                'flushes': 717,
                'last_finished': '1463693902',
                'last_ms': 2,
                'total_ms': 3630
            },
            'connections': {
                'available': 838846,
                'current': 14,
                'totalCreated': 3357
            },
            'cursors': {
                'clientCursors_size': 2,
                'note': 'deprecated, use server status metrics',
                'pinned': 0,
                'timedOut': 10,
                'totalNoTimeout': 0,
                'totalOpen': 2
            },
            'globalLock': {
                'activeClients': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'currentQueue': {
                    'readers': 0,
                    'total': 0,
                    'writers': 0
                },
                'lockTime': 17428935,
                'totalTime': 132516471000
            },
            'indexCounters': {
                'accesses': 581085,
                'hits': 581082,
                'missRatio': 0.0,
                'misses': 0,
                'resets': 0
            },
            'locks': {
                '.': {
                    'timeAcquiringMicros': {
                        'R': 5968032,
                        'W': 85482840
                    },
                    'timeLockedMicros': {
                        'R': 3735896,
                        'W': 17428935,
                        'r': 0,
                        'w': 567667
                    }
                },
                'admin': {
                    'timeAcquiringMicros': {
                        'r': 1274127,
                        'w': 0
                    },
                    'timeLockedMicros': {
                        'r': 49306822,
                        'w': 0
                    }
                },
                'local': {
                    'timeAcquiringMicros': {
                        'r': 186079130,
                        'w': 150543
                    },
                    'timeLockedMicros': {
                        'r': 289353029,
                        'w': 3202621
                    }
                },
                'main': {
                    'timeAcquiringMicros': {
                        'r': 1441131,
                        'w': 112204
                    },
                    'timeLockedMicros': {
                        'r': 44431521,
                        'w': 2502893
                    }
                },
                'zips': {
                    'timeAcquiringMicros': {
                        'r': 5,
                        'w': 0
                    },
                    'timeLockedMicros': {
                        'r': 839,
                        'w': 0
                    }
                }
            },
            'metrics': {
                'cursor': {
                    'open': {
                        'noTimeout': 0,
                        'pinned': 0,
                        'total': 2
                    },
                    'timedOut': 10
                },
                'document': {
                    'deleted': 0,
                    'inserted': 1,
                    'returned': 28,
                    'updated': 0
                },
                'getLastError': {
                    'wtime': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'wtimeouts': 0
                },
                'operation': {
                    'fastmod': 0,
                    'idhack': 0,
                    'scanAndOrder': 0
                },
                'queryExecutor': {
                    'scanned': 159,
                    'scannedObjects': 159
                },
                'record': {
                    'moves': 1
                },
                'repl': {
                    'apply': {
                        'batches': {
                            'num': 3106,
                            'totalMillis': 2754
                        },
                        'ops': 80272
                    },
                    'buffer': {
                        'count': 0,
                        'maxSizeBytes': 268435456,
                        'sizeBytes': 0
                    },
                    'network': {
                        'bytes': 29979685,
                        'getmores': {
                            'num': 10088,
                            'totalMillis': 69667749
                        },
                        'ops': 80271,
                        'readersCreated': 43
                    },
                    'preload': {
                        'docs': {
                            'num': 0,
                            'totalMillis': 0
                        },
                        'indexes': {
                            'num': 105816,
                            'totalMillis': 198
                        }
                    }
                },
                'storage': {
                    'freelist': {
                        'search': {
                            'bucketExhausted': 0,
                            'requests': 80788,
                            'scanned': 161556
                        }
                    }
                },
                'ttl': {
                    'deletedDocuments': 0,
                    'passes': 715
                }
            },
            'network': {
                'bytesIn': 8874058,
                'bytesOut': 19295455,
                'numRequests': 57486
            },
            'ok': 1.0,
            'opcounters': {
                'command': 53663,
                'delete': 0,
                'getmore': 3800,
                'insert': 1,
                'query': 2177,
                'update': 0
            },
            'opcountersRepl': {
                'command': 6,
                'delete': 0,
                'getmore': 0,
                'insert': 80266,
                'query': 0,
                'update': 0
            },
            'pid': 1,
            'recordStats': {
                'accessesNotInMemory': 3,
                'admin': {
                    'accessesNotInMemory': 3,
                    'pageFaultExceptionsThrown': 0
                },
                'local': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'main': {
                    'accessesNotInMemory': 0,
                    'pageFaultExceptionsThrown': 0
                },
                'pageFaultExceptionsThrown': 0
            },
            'uptime': 132517.0,
            'uptimeMillis': 132516471,
            'version': '2.6.11',
            'writeBacksQueued': False
        }
    }
}

INSTANCE_STATS_THIS_SECOND = {
    'aggregate_server_statistics': {
        'asserts': {
            'msg': 0,
            'regular': 0,
            'rollovers': 0,
            'user': 35,
            'warning': 0
        },
        'backgroundFlushing': {
            'average_ms': 23,
            'flushes': 1581,
            'last_finished': '1463693940',
            'last_ms': 6,
            'total_ms': 11327
        },
        'connections': {
            'available': 838846,
            'current': 14,
            'totalCreated': 3357
        },
        'cursors': {
            'clientCursors_size': 6,
            'note': 'deprecated, use server status metrics',
            'pinned': 0,
            'timedOut': 36,
            'totalNoTimeout': 0,
            'totalOpen': 6
        },
        'globalLock': {
            'activeClients': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'currentQueue': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'lockTime': 79785797,
            'totalTime': 290151795000
        },
        'indexCounters': {
            'accesses': 906465,
            'hits': 906462,
            'missRatio': 0,
            'misses': 0,
            'resets': 0
        },
        'locks': {
            '.': {
                'timeAcquiringMicros': {
                    'R': 29745476,
                    'W': 548660654
                },
                'timeLockedMicros': {
                    'R': 9227315,
                    'W': 79785797,
                    'r': 0,
                    'w': 637653
                }
            },
            'admin': {
                'timeAcquiringMicros': {
                    'r': 26330551,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 250271517,
                    'w': 0
                }
            },
            'local': {
                'timeAcquiringMicros': {
                    'r': 1486551269,
                    'w': 437781
                },
                'timeLockedMicros': {
                    'r': 1719837787,
                    'w': 6402458
                }
            },
            'main': {
                'timeAcquiringMicros': {
                    'r': 63139846,
                    'w': 222307
                },
                'timeLockedMicros': {
                    'r': 301844030,
                    'w': 5880379
                }
            },
            'zips': {
                'timeAcquiringMicros': {
                    'r': 5,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 839,
                    'w': 0
                }
            }
        },
        'metrics': {
            'cursor': {
                'open': {
                    'noTimeout': 0,
                    'pinned': 0,
                    'total': 6
                },
                'timedOut': 36
            },
            'document': {
                'deleted': 0,
                'inserted': 6404,
                'returned': 25585,
                'updated': 63
            },
            'getLastError': {
                'wtime': {
                    'num': 0,
                    'totalMillis': 0
                },
                'wtimeouts': 0
            },
            'operation': {
                'fastmod': 60,
                'idhack': 0,
                'scanAndOrder': 0
            },
            'queryExecutor': {
                'scanned': 25510,
                'scannedObjects': 25510
            },
            'record': {
                'moves': 2
            },
            'repl': {
                'apply': {
                    'batches': {
                        'num': 9737,
                        'totalMillis': 4693
                    },
                    'ops': 105367
                },
                'buffer': {
                    'count': 0,
                    'maxSizeBytes': 805306368,
                    'sizeBytes': 0
                },
                'network': {
                    'bytes': 40237384,
                    'getmores': {
                        'num': 20487,
                        'totalMillis': 87808215
                    },
                    'ops': 105365,
                    'readersCreated': 76
                },
                'preload': {
                    'docs': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'indexes': {
                        'num': 155998,
                        'totalMillis': 336
                    }
                }
            },
            'storage': {
                'freelist': {
                    'search': {
                        'bucketExhausted': 0,
                        'requests': 112708,
                        'scanned': 222866
                    }
                }
            },
            'ttl': {
                'deletedDocuments': 0,
                'passes': 1569
            }
        },
        'network': {
            'bytesIn': 26947059,
            'bytesOut': 70231076,
            'numRequests': 174796
        },
        'ok': 3,
        'opcounters': {
            'command': 144061,
            'delete': 0,
            'getmore': 30122,
            'insert': 6417,
            'query': 4792,
            'update': 63
        },
        'opcountersRepl': {
            'command': 7,
            'delete': 6325,
            'getmore': 0,
            'insert': 99035,
            'query': 0,
            'update': 0
        },
        'pid': 3,
        'recordStats': {
            'accessesNotInMemory': 14,
            'admin': {
                'accessesNotInMemory': 4,
                'pageFaultExceptionsThrown': 0
            },
            'local': {
                'accessesNotInMemory': 0,
                'pageFaultExceptionsThrown': 0
            },
            'main': {
                'accessesNotInMemory': 10,
                'pageFaultExceptionsThrown': 0
            },
            'pageFaultExceptionsThrown': 0
        },
        'uptime': 290152,
        'uptimeMillis': 290151792,
        'version': '2.6.11',
        'writeBacksQueued': 0
    },
    'opcounters_per_node': [{
        '4d558d4e694249cba6352252dbc7e443': {
            'iad1clus01br0vz544.iad1.devtools:33544': {
                'command': 51321,
                'delete': 0,
                'getmore': 22558,
                'insert': 6415,
                'query': 1236,
                'update': 63
            },
            'iad1clus01br0vz588.iad1.devtools:33588': {
                'command': 28827,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1190,
                'update': 0
            },
            'iad1clus01br0vz770.iad1.devtools:32770': {
                'command': 28856,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1191,
                'update': 0
            }
        }
    }, {
        '356a9912480f4d8a8ac032eb89d1ce81': {
            'iad1clus01br0vz291.iad1.devtools:33291': {
                'command': 59669,
                'delete': 0,
                'getmore': 20661,
                'insert': 18768,
                'query': 1419,
                'update': 71
            },
            'iad1clus01br0vz609.iad1.devtools:33609': {
                'command': 36060,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1354,
                'update': 0
            },
            'iad1clus01br0vz976.iad1.devtools:32976': {
                'command': 39095,
                'delete': 0,
                'getmore': 3764,
                'insert': 1,
                'query': 1379,
                'update': 0
            }
        }
    }, {
        'e4f8cc3415954cb98852c98fd659ce95': {
            'iad1clus01br0vz369.iad1.devtools:33369': {
                'command': 77125,
                'delete': 0,
                'getmore': 20234,
                'insert': 80266,
                'query': 2267,
                'update': 85
            },
            'iad1clus01br0vz505.iad1.devtools:33505': {
                'command': 53672,
                'delete': 0,
                'getmore': 3800,
                'insert': 1,
                'query': 2177,
                'update': 0
            },
            'iad1clus01br0vz851.iad1.devtools:32851': {
                'command': 50605,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 2165,
                'update': 0
            }
        }
    }],
    'replication_lag': 0.0
}


INSTANCE_STATS_NEXT_SECOND = {
    'aggregate_server_statistics': {
        'asserts': {
            'msg': 0,
            'regular': 0,
            'rollovers': 0,
            'user': 35,
            'warning': 0
        },
        'backgroundFlushing': {
            'average_ms': 23,
            'flushes': 1581,
            'last_finished': '1463693940',
            'last_ms': 6,
            'total_ms': 11327
        },
        'connections': {
            'available': 838846,
            'current': 14,
            'totalCreated': 3357
        },
        'cursors': {
            'clientCursors_size': 6,
            'note': 'deprecated, use server status metrics',
            'pinned': 0,
            'timedOut': 36,
            'totalNoTimeout': 0,
            'totalOpen': 6
        },
        'globalLock': {
            'activeClients': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'currentQueue': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'lockTime': 79785797,
            'totalTime': 290151795000
        },
        'indexCounters': {
            'accesses': 906465,
            'hits': 906462,
            'missRatio': 0,
            'misses': 0,
            'resets': 0
        },
        'locks': {
            '.': {
                'timeAcquiringMicros': {
                    'R': 29745476,
                    'W': 548660654
                },
                'timeLockedMicros': {
                    'R': 9227315,
                    'W': 79785797,
                    'r': 0,
                    'w': 637653
                }
            },
            'admin': {
                'timeAcquiringMicros': {
                    'r': 26330551,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 250271517,
                    'w': 0
                }
            },
            'local': {
                'timeAcquiringMicros': {
                    'r': 1486551269,
                    'w': 437781
                },
                'timeLockedMicros': {
                    'r': 1719837787,
                    'w': 6402458
                }
            },
            'main': {
                'timeAcquiringMicros': {
                    'r': 63139846,
                    'w': 222307
                },
                'timeLockedMicros': {
                    'r': 301844030,
                    'w': 5880379
                }
            },
            'zips': {
                'timeAcquiringMicros': {
                    'r': 5,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 839,
                    'w': 0
                }
            }
        },
        'metrics': {
            'cursor': {
                'open': {
                    'noTimeout': 0,
                    'pinned': 0,
                    'total': 6
                },
                'timedOut': 36
            },
            'document': {
                'deleted': 0,
                'inserted': 6404,
                'returned': 25585,
                'updated': 63
            },
            'getLastError': {
                'wtime': {
                    'num': 0,
                    'totalMillis': 0
                },
                'wtimeouts': 0
            },
            'operation': {
                'fastmod': 60,
                'idhack': 0,
                'scanAndOrder': 0
            },
            'queryExecutor': {
                'scanned': 25510,
                'scannedObjects': 25510
            },
            'record': {
                'moves': 2
            },
            'repl': {
                'apply': {
                    'batches': {
                        'num': 9737,
                        'totalMillis': 4693
                    },
                    'ops': 105367
                },
                'buffer': {
                    'count': 0,
                    'maxSizeBytes': 805306368,
                    'sizeBytes': 0
                },
                'network': {
                    'bytes': 40237384,
                    'getmores': {
                        'num': 20487,
                        'totalMillis': 87808215
                    },
                    'ops': 105365,
                    'readersCreated': 76
                },
                'preload': {
                    'docs': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'indexes': {
                        'num': 155998,
                        'totalMillis': 336
                    }
                }
            },
            'storage': {
                'freelist': {
                    'search': {
                        'bucketExhausted': 0,
                        'requests': 112708,
                        'scanned': 222866
                    }
                }
            },
            'ttl': {
                'deletedDocuments': 0,
                'passes': 1569
            }
        },
        'network': {
            'bytesIn': 26947059,
            'bytesOut': 70231076,
            'numRequests': 174796
        },
        'ok': 3,
        'opcounters': {
            'command': 144061,
            'delete': 0,
            'getmore': 30122,
            'insert': 6417,
            'query': 4792,
            'update': 63
        },
        'opcountersRepl': {
            'command': 7,
            'delete': 6325,
            'getmore': 0,
            'insert': 99035,
            'query': 0,
            'update': 0
        },
        'pid': 3,
        'recordStats': {
            'accessesNotInMemory': 14,
            'admin': {
                'accessesNotInMemory': 4,
                'pageFaultExceptionsThrown': 0
            },
            'local': {
                'accessesNotInMemory': 0,
                'pageFaultExceptionsThrown': 0
            },
            'main': {
                'accessesNotInMemory': 10,
                'pageFaultExceptionsThrown': 0
            },
            'pageFaultExceptionsThrown': 0
        },
        'uptime': 290152,
        'uptimeMillis': 290151792,
        'version': '2.6.11',
        'writeBacksQueued': 0
    },
    'opcounters_per_node': [{
        '4d558d4e694249cba6352252dbc7e443': {
            'iad1clus01br0vz544.iad1.devtools:33544': {
                'command': 51321,
                'delete': 0,
                'getmore': 22558,
                'insert': 6415,
                'query': 1236,
                'update': 63
            },
            'iad1clus01br0vz588.iad1.devtools:33588': {
                'command': 28827,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1190,
                'update': 0
            },
            'iad1clus01br0vz770.iad1.devtools:32770': {
                'command': 28856,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1191,
                'update': 0
            }
        }
    }, {
        '356a9912480f4d8a8ac032eb89d1ce81': {
            'iad1clus01br0vz291.iad1.devtools:33291': {
                'command': 59669,
                'delete': 0,
                'getmore': 20661,
                'insert': 18768,
                'query': 1419,
                'update': 71
            },
            'iad1clus01br0vz609.iad1.devtools:33609': {
                'command': 36060,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 1354,
                'update': 0
            },
            'iad1clus01br0vz976.iad1.devtools:32976': {
                'command': 39095,
                'delete': 0,
                'getmore': 3764,
                'insert': 1,
                'query': 1379,
                'update': 0
            }
        }
    }, {
        'e4f8cc3415954cb98852c98fd659ce95': {
            'iad1clus01br0vz369.iad1.devtools:33369': {
                'command': 77125,
                'delete': 0,
                'getmore': 20234,
                'insert': 80266,
                'query': 2267,
                'update': 85
            },
            'iad1clus01br0vz505.iad1.devtools:33505': {
                'command': 53672,
                'delete': 0,
                'getmore': 3800,
                'insert': 1,
                'query': 2177,
                'update': 0
            },
            'iad1clus01br0vz851.iad1.devtools:32851': {
                'command': 50605,
                'delete': 0,
                'getmore': 0,
                'insert': 1,
                'query': 2165,
                'update': 0
            }
        }
    }],
    'replication_lag': 0.0
}


NEW_RELIC_STATS = {
    'aggregate_database_statistics': {
        'avgObjSize': 620,
        'dataSize': 47486228,
        'fileSize': 167772160,
        'indexSize': 5943952,
        'indexes': 27,
        'nsSize': 33554432,
        'numExtents': 51,
        'objects': 105544,
        'storageSize': 89194496
    },
    'aggregate_server_statistics': {
        'asserts': {
            'msg': 0,
            'regular': 0,
            'rollovers': 0,
            'user': 35,
            'warning': 0
        },
        'backgroundFlushing': {
            'average_ms': 23,
            'flushes': 1581,
            'last_finished': '1463693940',
            'last_ms': 6,
            'total_ms': 11327
        },
        'connections': {
            'available': 838846,
            'current': 14,
            'totalCreated': 3357
        },
        'cursors': {
            'clientCursors_size': 6,
            'note': 'deprecated, use server status metrics',
            'pinned': 0,
            'timedOut': 36,
            'totalNoTimeout': 0,
            'totalOpen': 6
        },
        'globalLock': {
            'activeClients': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'currentQueue': {
                'readers': 0,
                'total': 0,
                'writers': 0
            },
            'lockTime': 79785797,
            'totalTime': 290151795000
        },
        'indexCounters': {
            'accesses': 906465,
            'hits': 906462,
            'missRatio': 0,
            'misses': 0,
            'resets': 0
        },
        'locks': {
            '.': {
                'timeAcquiringMicros': {
                    'R': 29745476,
                    'W': 548660654
                },
                'timeLockedMicros': {
                    'R': 9227315,
                    'W': 79785797,
                    'r': 0,
                    'w': 637653
                }
            },
            'admin': {
                'timeAcquiringMicros': {
                    'r': 26330551,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 250271517,
                    'w': 0
                }
            },
            'local': {
                'timeAcquiringMicros': {
                    'r': 1486551269,
                    'w': 437781
                },
                'timeLockedMicros': {
                    'r': 1719837787,
                    'w': 6402458
                }
            },
            'main': {
                'timeAcquiringMicros': {
                    'r': 63139846,
                    'w': 222307
                },
                'timeLockedMicros': {
                    'r': 301844030,
                    'w': 5880379
                }
            },
            'zips': {
                'timeAcquiringMicros': {
                    'r': 5,
                    'w': 0
                },
                'timeLockedMicros': {
                    'r': 839,
                    'w': 0
                }
            }
        },
        'metrics': {
            'cursor': {
                'open': {
                    'noTimeout': 0,
                    'pinned': 0,
                    'total': 6
                },
                'timedOut': 36
            },
            'document': {
                'deleted': 0,
                'inserted': 6404,
                'returned': 25585,
                'updated': 63
            },
            'getLastError': {
                'wtime': {
                    'num': 0,
                    'totalMillis': 0
                },
                'wtimeouts': 0
            },
            'operation': {
                'fastmod': 60,
                'idhack': 0,
                'scanAndOrder': 0
            },
            'queryExecutor': {
                'scanned': 25510,
                'scannedObjects': 25510
            },
            'record': {
                'moves': 2
            },
            'repl': {
                'apply': {
                    'batches': {
                        'num': 9737,
                        'totalMillis': 4693
                    },
                    'ops': 105367
                },
                'buffer': {
                    'count': 0,
                    'maxSizeBytes': 805306368,
                    'sizeBytes': 0
                },
                'network': {
                    'bytes': 40237384,
                    'getmores': {
                        'num': 20487,
                        'totalMillis': 87808215
                    },
                    'ops': 105365,
                    'readersCreated': 76
                },
                'preload': {
                    'docs': {
                        'num': 0,
                        'totalMillis': 0
                    },
                    'indexes': {
                        'num': 155998,
                        'totalMillis': 336
                    }
                }
            },
            'storage': {
                'freelist': {
                    'search': {
                        'bucketExhausted': 0,
                        'requests': 112708,
                        'scanned': 222866
                    }
                }
            },
            'ttl': {
                'deletedDocuments': 0,
                'passes': 1569
            }
        },
        'network': {
            'bytesIn': 26947059,
            'bytesOut': 70231076,
            'numRequests': 174796
        },
        'ok': 3,
        'opcounters': {
            'command': 144061,
            'delete': 0,
            'getmore': 30122,
            'insert': 6417,
            'query': 4792,
            'update': 63
        },
        'opcountersRepl': {
            'command': 7,
            'delete': 6325,
            'getmore': 0,
            'insert': 99035,
            'query': 0,
            'update': 0
        },
        'pid': 3,
        'recordStats': {
            'accessesNotInMemory': 14,
            'admin': {
                'accessesNotInMemory': 4,
                'pageFaultExceptionsThrown': 0
            },
            'local': {
                'accessesNotInMemory': 0,
                'pageFaultExceptionsThrown': 0
            },
            'main': {
                'accessesNotInMemory': 10,
                'pageFaultExceptionsThrown': 0
            },
            'pageFaultExceptionsThrown': 0
        },
        'uptime': 290152,
        'uptimeMillis': 290151792,
        'version': '2.6.11',
        'writeBacksQueued': 0
    },
    'opcounters_per_node_per_second': [{
        '4d558d4e694249cba6352252dbc7e443': {
            'iad1clus01br0vz544.iad1.devtools:33544': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz588.iad1.devtools:33588': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz770.iad1.devtools:32770': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            }
        }
    }, {
        '356a9912480f4d8a8ac032eb89d1ce81': {
            'iad1clus01br0vz291.iad1.devtools:33291': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz609.iad1.devtools:33609': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz976.iad1.devtools:32976': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            }
        }
    }, {
        'e4f8cc3415954cb98852c98fd659ce95': {
            'iad1clus01br0vz369.iad1.devtools:33369': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz505.iad1.devtools:33505': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            },
            'iad1clus01br0vz851.iad1.devtools:32851': {
                'command': 0,
                'delete': 0,
                'getmore': 0,
                'insert': 0,
                'query': 0,
                'update': 0
            }
        }
    }],
    'replication_lag': 0.0,
    'server_statistics_per_second': {
        'network': {
            'bytesIn': 0,
            'bytesOut': 0,
            'numRequests': 0
        },
        'opcounters': {
            'command': 0,
            'delete': 0,
            'getmore': 0,
            'insert': 0,
            'query': 0,
            'update': 0
        }
    }
}
