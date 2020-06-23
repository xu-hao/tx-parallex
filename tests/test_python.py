from tx.parallex.python import python_to_spec
from tx.functional.either import Left, Right

def test_python_to_spec1():
    py = "a = mod1.mod2.func(param=arg)"
    spec = python_to_spec(py)
    assert spec == {
        "type": "python",
        "name": "a",
        "mod": "mod1.mod2",
        "func": "func",
        "params": {
            "param": {
                "name": "arg"
            }
        }
    }


def test_python_to_spec2():
    py = """
var = mod3.func2()
a = mod1.mod2.func(param=var)"""
    spec = python_to_spec(py)
    assert spec == {
        "type":"top",
        "sub": [{
            "type": "python",
            "name": "var",
            "mod": "mod3",
            "func": "func2",
            "params": {}
        }, {
            "type": "python",
            "name": "a",
            "mod": "mod1.mod2",
            "func": "func",
            "params": {
                "param": {
                    "depends_on": "var"
                }
            }
        }]       
    }

def test_python_to_spec3():
    py = """
var = mod3.func2()
a = mod1.mod2.func(param=var)
return {'ret1': a}"""
    spec = python_to_spec(py)
    assert spec == {
        "type":"top",
        "sub": [{
            "type": "python",
            "name": "var",
            "mod": "mod3",
            "func": "func2",
            "params": {}
        }, {
            "type": "python",
            "name": "a",
            "mod": "mod1.mod2",
            "func": "func",
            "params": {
                "param": {
                    "depends_on": "var"
                }
            }
        }, {
            "type": "ret",
            "var": "ret1",
            "obj": {
                "depends_on": "a"
            }
        }]
    }

def test_python_to_spec4():
    py = "a = 1"
    spec = python_to_spec(py)
    assert spec == {
        "type":"let",
        "var": "a",
        "obj": {
            "data": 1
        },
        "sub": {
            "type": "top",
            "sub": []
        }
    }


def test_python_to_spec5():
    py = """
for i in c:
    x = mod1.func2(r=i)"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "map",
        "var": "i",
        "coll": {
            "name": "c"
        },
        "sub": {
                "type": "python",
                "name": "x",
                "mod": "mod1",
                "func": "func2",
                "params": {
                    "r": {
                        "name": "i"
                    }
                }
        }
    }

    
def test_python_to_spec6():
    py = """
y = 1
for i in c:
    x = mod1.func2(r=i)"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "y",
        "obj": {
            "data": 1
        },
        "sub": {
            "type": "map",
            "var": "i",
            "coll": {
                "name": "c"
            },
            "sub": {
                    "type": "python",
                    "name": "x",
                    "mod": "mod1",
                    "func": "func2",
                    "params": {
                        "r": {
                            "name": "i"
                        }
                    }
            }
        }
    }

def test_python_to_spec7():
    py = """
y = 1
for i in c:
    for j in d:
        x = mod1.func2(s=i,t=j)"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "y",
        "obj": {
            "data": 1
        },
        "sub": {
            "type": "map",
            "var": "i",
            "coll": {
                "name": "c"
            },
            "sub": {
                "type": "map",
                "var": "j",
                "coll": {
                    "name": "d"
                },
                "sub": {
                        "type": "python",
                        "name": "x",
                        "mod": "mod1",
                        "func": "func2",
                        "params": {
                            "s": {
                                "name": "i"
                            },
                            "t": {
                                "name": "j"
                            }
                        }
                }
            }
        }
    }

def test_python_to_spec8():
    py = """
y = 4
for i in c:
    z = 390
    for j in d:
        x = mod1.func2(s=i,t=j)"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "y",
        "obj": {
            "data": 4
        },
        "sub": {
            "type": "map",
            "var": "i",
            "coll": {
                "name": "c"
            },
            "sub": {
                "type": "let",
                "var": "z",
                "obj": {
                    "data": 390
                },
                "sub": {
                    "type": "map",
                    "var": "j",
                    "coll": {
                        "name": "d"
                    },
                    "sub": {
                            "type": "python",
                            "name": "x",
                            "mod": "mod1",
                            "func": "func2",
                            "params": {
                                "s": {
                                    "name": "i"
                                },
                                "t": {
                                    "name": "j"
                                }
                            }
                    }
                }
            }
        }
    }

def test_python_to_spec9():
    py = """
y = mod2.func3(x)
for i in c:
    x = mod1.func2(u=y)"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "top",
        "sub": [{
            "type": "python",
            "name": "y",
            "mod": "mod2",
            "func": "func3",
            "params": {
                0: {
                    "name": "x"
                }
            }
        }, {
            "type": "map",
            "var": "i",
            "coll": {
                "name": "c"
            },
            "sub": {
                "type": "python",
                "name": "x",
                "mod": "mod1",
                "func": "func2",
                "params": {
                    "u": {
                        "depends_on": "y"
                    }
                }
            }
        }]
    }

def test_python_to_spec10():
    py = """x = mod1.func2(i)"""

    spec = python_to_spec(py)
    assert spec == {
            "type": "python",
            "name": "x",
            "mod": "mod1",
            "func": "func2",
            "params": {
                0: {
                    "name": "i"
                }
            }
    }

def test_python_to_spec11():
    py = """
d = [2,3]
c = tests.test_task.identity(d)
for j in c:
    a = tests.test_task.g(x=2,y=j)
    return {"x": a}"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "d",
        "obj": {
            "data": [2,3]
        },
        "sub": {
            "type": "top",
            "sub": [{
                "type": "python",
                "name": "c",
                "mod": "tests.test_task",
                "func": "identity",
                "params": {
                    0: {
                        "name": "d"
                    }
                }
            }, {
                "type": "map",
                "var": "j",
                "coll": {
                    "depends_on": "c"
                },
                "sub": {
                    "type": "top",
                    "sub": [{
                        "type": "python",
                        "name": "a",
                        "mod": "tests.test_task",
                        "func": "g",
                        "params": {
                            "x": {
                                "data": 2
                            },
                            "y": {
                                "name": "j"
                            }
                        }
                    }, {
                        "type": "ret",
                        "var": "x",
                        "obj": {
                            "depends_on": "a"
                        }
                    }]
                }
            }]
        }
    }

def test_python_to_spec12():
    py = """
z = True
if z:
    return {
        "x": 1
    }
else:
    return {
        "x": 0
    }"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "z",
        "obj": {
            "data": True
        },
        "sub": {
            "type": "cond",
            "on": {
                "name": "z"
            },
            "then": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 1
                }
            },
            "else": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 0
                }
            }
        }
    }
    

def test_python_to_spec13():
    py = """
z = False
if z:
    return {
        "x": 1
    }
else:
    return {
        "x": 0
    }"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "let",
        "var": "z",
        "obj": {
            "data": False
        },
        "sub": {
            "type": "cond",
            "on": {
                "name": "z"
            },
            "then": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 1
                }
            },
            "else": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 0
                }
            }
        }
    }
    

def test_python_to_spec14():
    py = """
z = tests.test_task.true()
if z:
    return {
        "x": 1
    }
else:
    return {
        "x": 0
    }"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "top",
        "sub": [{
            "type": "python",
            "name": "z",
            "mod": "tests.test_task",
            "func": "true",
            "params": {
            }
        }, {
            "type": "cond",
            "on": {
                "depends_on": "z"
            },
            "then": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 1
                }
            },
            "else": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 0
                }
            }
        }]
    }


def test_python_to_spec15():
    py = """
z = tests.test_task.false()
if z:
    return {
        "x": 1
    }
else:
    return {
        "x": 0
    }"""

    spec = python_to_spec(py)
    assert spec == {
        "type": "top",
        "sub": [{
            "type": "python",
            "name": "z",
            "mod": "tests.test_task",
            "func": "false",
            "params": {
            }
        }, {
            "type": "cond",
            "on": {
                "depends_on": "z"
            },
            "then": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 1
                }
            },
            "else": {
                "type": "ret",
                "var": "x",
                "obj": {
                    "data": 0
                }
            }
        }]
    }


