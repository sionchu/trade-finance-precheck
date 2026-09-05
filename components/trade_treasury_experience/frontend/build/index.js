var Hr = { exports: {} }, sl = {};
var ry;
function X1() {
  if (ry) return sl;
  ry = 1;
  var i = /* @__PURE__ */ Symbol.for("react.transitional.element"), l = /* @__PURE__ */ Symbol.for("react.fragment");
  function u(o, c, d) {
    var h = null;
    if (d !== void 0 && (h = "" + d), c.key !== void 0 && (h = "" + c.key), "key" in c) {
      d = {};
      for (var y in c)
        y !== "key" && (d[y] = c[y]);
    } else d = c;
    return c = d.ref, {
      $$typeof: i,
      type: o,
      key: h,
      ref: c !== void 0 ? c : null,
      props: d
    };
  }
  return sl.Fragment = l, sl.jsx = u, sl.jsxs = u, sl;
}
var cy;
function Z1() {
  return cy || (cy = 1, Hr.exports = X1()), Hr.exports;
}
var rt = Z1(), Yr = { exports: {} }, at = {};
var fy;
function Q1() {
  if (fy) return at;
  fy = 1;
  var i = /* @__PURE__ */ Symbol.for("react.transitional.element"), l = /* @__PURE__ */ Symbol.for("react.portal"), u = /* @__PURE__ */ Symbol.for("react.fragment"), o = /* @__PURE__ */ Symbol.for("react.strict_mode"), c = /* @__PURE__ */ Symbol.for("react.profiler"), d = /* @__PURE__ */ Symbol.for("react.consumer"), h = /* @__PURE__ */ Symbol.for("react.context"), y = /* @__PURE__ */ Symbol.for("react.forward_ref"), g = /* @__PURE__ */ Symbol.for("react.suspense"), m = /* @__PURE__ */ Symbol.for("react.memo"), v = /* @__PURE__ */ Symbol.for("react.lazy"), S = /* @__PURE__ */ Symbol.for("react.activity"), b = Symbol.iterator;
  function _(E) {
    return E === null || typeof E != "object" ? null : (E = b && E[b] || E["@@iterator"], typeof E == "function" ? E : null);
  }
  var z = {
    isMounted: function() {
      return !1;
    },
    enqueueForceUpdate: function() {
    },
    enqueueReplaceState: function() {
    },
    enqueueSetState: function() {
    }
  }, j = Object.assign, w = {};
  function L(E, N, Z) {
    this.props = E, this.context = N, this.refs = w, this.updater = Z || z;
  }
  L.prototype.isReactComponent = {}, L.prototype.setState = function(E, N) {
    if (typeof E != "object" && typeof E != "function" && E != null)
      throw Error(
        "takes an object of state variables to update or a function which returns an object of state variables."
      );
    this.updater.enqueueSetState(this, E, N, "setState");
  }, L.prototype.forceUpdate = function(E) {
    this.updater.enqueueForceUpdate(this, E, "forceUpdate");
  };
  function G() {
  }
  G.prototype = L.prototype;
  function H(E, N, Z) {
    this.props = E, this.context = N, this.refs = w, this.updater = Z || z;
  }
  var Y = H.prototype = new G();
  Y.constructor = H, j(Y, L.prototype), Y.isPureReactComponent = !0;
  var tt = Array.isArray;
  function nt() {
  }
  var Q = { H: null, A: null, T: null, S: null }, K = Object.prototype.hasOwnProperty;
  function it(E, N, Z) {
    var W = Z.ref;
    return {
      $$typeof: i,
      type: E,
      key: N,
      ref: W !== void 0 ? W : null,
      props: Z
    };
  }
  function $(E, N) {
    return it(E.type, N, E.props);
  }
  function yt(E) {
    return typeof E == "object" && E !== null && E.$$typeof === i;
  }
  function vt(E) {
    var N = { "=": "=0", ":": "=2" };
    return "$" + E.replace(/[=:]/g, function(Z) {
      return N[Z];
    });
  }
  var Pt = /\/+/g;
  function qt(E, N) {
    return typeof E == "object" && E !== null && E.key != null ? vt("" + E.key) : N.toString(36);
  }
  function wt(E) {
    switch (E.status) {
      case "fulfilled":
        return E.value;
      case "rejected":
        throw E.reason;
      default:
        switch (typeof E.status == "string" ? E.then(nt, nt) : (E.status = "pending", E.then(
          function(N) {
            E.status === "pending" && (E.status = "fulfilled", E.value = N);
          },
          function(N) {
            E.status === "pending" && (E.status = "rejected", E.reason = N);
          }
        )), E.status) {
          case "fulfilled":
            return E.value;
          case "rejected":
            throw E.reason;
        }
    }
    throw E;
  }
  function O(E, N, Z, W, lt) {
    var ct = typeof E;
    (ct === "undefined" || ct === "boolean") && (E = null);
    var At = !1;
    if (E === null) At = !0;
    else
      switch (ct) {
        case "bigint":
        case "string":
        case "number":
          At = !0;
          break;
        case "object":
          switch (E.$$typeof) {
            case i:
            case l:
              At = !0;
              break;
            case v:
              return At = E._init, O(
                At(E._payload),
                N,
                Z,
                W,
                lt
              );
          }
      }
    if (At)
      return lt = lt(E), At = W === "" ? "." + qt(E, 0) : W, tt(lt) ? (Z = "", At != null && (Z = At.replace(Pt, "$&/") + "/"), O(lt, N, Z, "", function(da) {
        return da;
      })) : lt != null && (yt(lt) && (lt = $(
        lt,
        Z + (lt.key == null || E && E.key === lt.key ? "" : ("" + lt.key).replace(
          Pt,
          "$&/"
        ) + "/") + At
      )), N.push(lt)), 1;
    At = 0;
    var se = W === "" ? "." : W + ":";
    if (tt(E))
      for (var Lt = 0; Lt < E.length; Lt++)
        W = E[Lt], ct = se + qt(W, Lt), At += O(
          W,
          N,
          Z,
          ct,
          lt
        );
    else if (Lt = _(E), typeof Lt == "function")
      for (E = Lt.call(E), Lt = 0; !(W = E.next()).done; )
        W = W.value, ct = se + qt(W, Lt++), At += O(
          W,
          N,
          Z,
          ct,
          lt
        );
    else if (ct === "object") {
      if (typeof E.then == "function")
        return O(
          wt(E),
          N,
          Z,
          W,
          lt
        );
      throw N = String(E), Error(
        "Objects are not valid as a React child (found: " + (N === "[object Object]" ? "object with keys {" + Object.keys(E).join(", ") + "}" : N) + "). If you meant to render a collection of children, use an array instead."
      );
    }
    return At;
  }
  function X(E, N, Z) {
    if (E == null) return E;
    var W = [], lt = 0;
    return O(E, W, "", "", function(ct) {
      return N.call(Z, ct, lt++);
    }), W;
  }
  function J(E) {
    if (E._status === -1) {
      var N = E._result;
      N = N(), N.then(
        function(Z) {
          (E._status === 0 || E._status === -1) && (E._status = 1, E._result = Z);
        },
        function(Z) {
          (E._status === 0 || E._status === -1) && (E._status = 2, E._result = Z);
        }
      ), E._status === -1 && (E._status = 0, E._result = N);
    }
    if (E._status === 1) return E._result.default;
    throw E._result;
  }
  var ut = typeof reportError == "function" ? reportError : function(E) {
    if (typeof window == "object" && typeof window.ErrorEvent == "function") {
      var N = new window.ErrorEvent("error", {
        bubbles: !0,
        cancelable: !0,
        message: typeof E == "object" && E !== null && typeof E.message == "string" ? String(E.message) : String(E),
        error: E
      });
      if (!window.dispatchEvent(N)) return;
    } else if (typeof process == "object" && typeof process.emit == "function") {
      process.emit("uncaughtException", E);
      return;
    }
    console.error(E);
  }, pt = {
    map: X,
    forEach: function(E, N, Z) {
      X(
        E,
        function() {
          N.apply(this, arguments);
        },
        Z
      );
    },
    count: function(E) {
      var N = 0;
      return X(E, function() {
        N++;
      }), N;
    },
    toArray: function(E) {
      return X(E, function(N) {
        return N;
      }) || [];
    },
    only: function(E) {
      if (!yt(E))
        throw Error(
          "React.Children.only expected to receive a single React element child."
        );
      return E;
    }
  };
  return at.Activity = S, at.Children = pt, at.Component = L, at.Fragment = u, at.Profiler = c, at.PureComponent = H, at.StrictMode = o, at.Suspense = g, at.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = Q, at.__COMPILER_RUNTIME = {
    __proto__: null,
    c: function(E) {
      return Q.H.useMemoCache(E);
    }
  }, at.cache = function(E) {
    return function() {
      return E.apply(null, arguments);
    };
  }, at.cacheSignal = function() {
    return null;
  }, at.cloneElement = function(E, N, Z) {
    if (E == null)
      throw Error(
        "The argument must be a React element, but you passed " + E + "."
      );
    var W = j({}, E.props), lt = E.key;
    if (N != null)
      for (ct in N.key !== void 0 && (lt = "" + N.key), N)
        !K.call(N, ct) || ct === "key" || ct === "__self" || ct === "__source" || ct === "ref" && N.ref === void 0 || (W[ct] = N[ct]);
    var ct = arguments.length - 2;
    if (ct === 1) W.children = Z;
    else if (1 < ct) {
      for (var At = Array(ct), se = 0; se < ct; se++)
        At[se] = arguments[se + 2];
      W.children = At;
    }
    return it(E.type, lt, W);
  }, at.createContext = function(E) {
    return E = {
      $$typeof: h,
      _currentValue: E,
      _currentValue2: E,
      _threadCount: 0,
      Provider: null,
      Consumer: null
    }, E.Provider = E, E.Consumer = {
      $$typeof: d,
      _context: E
    }, E;
  }, at.createElement = function(E, N, Z) {
    var W, lt = {}, ct = null;
    if (N != null)
      for (W in N.key !== void 0 && (ct = "" + N.key), N)
        K.call(N, W) && W !== "key" && W !== "__self" && W !== "__source" && (lt[W] = N[W]);
    var At = arguments.length - 2;
    if (At === 1) lt.children = Z;
    else if (1 < At) {
      for (var se = Array(At), Lt = 0; Lt < At; Lt++)
        se[Lt] = arguments[Lt + 2];
      lt.children = se;
    }
    if (E && E.defaultProps)
      for (W in At = E.defaultProps, At)
        lt[W] === void 0 && (lt[W] = At[W]);
    return it(E, ct, lt);
  }, at.createRef = function() {
    return { current: null };
  }, at.forwardRef = function(E) {
    return { $$typeof: y, render: E };
  }, at.isValidElement = yt, at.lazy = function(E) {
    return {
      $$typeof: v,
      _payload: { _status: -1, _result: E },
      _init: J
    };
  }, at.memo = function(E, N) {
    return {
      $$typeof: m,
      type: E,
      compare: N === void 0 ? null : N
    };
  }, at.startTransition = function(E) {
    var N = Q.T, Z = {};
    Q.T = Z;
    try {
      var W = E(), lt = Q.S;
      lt !== null && lt(Z, W), typeof W == "object" && W !== null && typeof W.then == "function" && W.then(nt, ut);
    } catch (ct) {
      ut(ct);
    } finally {
      N !== null && Z.types !== null && (N.types = Z.types), Q.T = N;
    }
  }, at.unstable_useCacheRefresh = function() {
    return Q.H.useCacheRefresh();
  }, at.use = function(E) {
    return Q.H.use(E);
  }, at.useActionState = function(E, N, Z) {
    return Q.H.useActionState(E, N, Z);
  }, at.useCallback = function(E, N) {
    return Q.H.useCallback(E, N);
  }, at.useContext = function(E) {
    return Q.H.useContext(E);
  }, at.useDebugValue = function() {
  }, at.useDeferredValue = function(E, N) {
    return Q.H.useDeferredValue(E, N);
  }, at.useEffect = function(E, N) {
    return Q.H.useEffect(E, N);
  }, at.useEffectEvent = function(E) {
    return Q.H.useEffectEvent(E);
  }, at.useId = function() {
    return Q.H.useId();
  }, at.useImperativeHandle = function(E, N, Z) {
    return Q.H.useImperativeHandle(E, N, Z);
  }, at.useInsertionEffect = function(E, N) {
    return Q.H.useInsertionEffect(E, N);
  }, at.useLayoutEffect = function(E, N) {
    return Q.H.useLayoutEffect(E, N);
  }, at.useMemo = function(E, N) {
    return Q.H.useMemo(E, N);
  }, at.useOptimistic = function(E, N) {
    return Q.H.useOptimistic(E, N);
  }, at.useReducer = function(E, N, Z) {
    return Q.H.useReducer(E, N, Z);
  }, at.useRef = function(E) {
    return Q.H.useRef(E);
  }, at.useState = function(E) {
    return Q.H.useState(E);
  }, at.useSyncExternalStore = function(E, N, Z) {
    return Q.H.useSyncExternalStore(
      E,
      N,
      Z
    );
  }, at.useTransition = function() {
    return Q.H.useTransition();
  }, at.version = "19.2.8", at;
}
var hy;
function _c() {
  return hy || (hy = 1, Yr.exports = Q1()), Yr.exports;
}
var q = _c(), qr = { exports: {} }, ul = {}, Gr = { exports: {} }, Xr = {};
var dy;
function K1() {
  return dy || (dy = 1, (function(i) {
    function l(O, X) {
      var J = O.length;
      O.push(X);
      t: for (; 0 < J; ) {
        var ut = J - 1 >>> 1, pt = O[ut];
        if (0 < c(pt, X))
          O[ut] = X, O[J] = pt, J = ut;
        else break t;
      }
    }
    function u(O) {
      return O.length === 0 ? null : O[0];
    }
    function o(O) {
      if (O.length === 0) return null;
      var X = O[0], J = O.pop();
      if (J !== X) {
        O[0] = J;
        t: for (var ut = 0, pt = O.length, E = pt >>> 1; ut < E; ) {
          var N = 2 * (ut + 1) - 1, Z = O[N], W = N + 1, lt = O[W];
          if (0 > c(Z, J))
            W < pt && 0 > c(lt, Z) ? (O[ut] = lt, O[W] = J, ut = W) : (O[ut] = Z, O[N] = J, ut = N);
          else if (W < pt && 0 > c(lt, J))
            O[ut] = lt, O[W] = J, ut = W;
          else break t;
        }
      }
      return X;
    }
    function c(O, X) {
      var J = O.sortIndex - X.sortIndex;
      return J !== 0 ? J : O.id - X.id;
    }
    if (i.unstable_now = void 0, typeof performance == "object" && typeof performance.now == "function") {
      var d = performance;
      i.unstable_now = function() {
        return d.now();
      };
    } else {
      var h = Date, y = h.now();
      i.unstable_now = function() {
        return h.now() - y;
      };
    }
    var g = [], m = [], v = 1, S = null, b = 3, _ = !1, z = !1, j = !1, w = !1, L = typeof setTimeout == "function" ? setTimeout : null, G = typeof clearTimeout == "function" ? clearTimeout : null, H = typeof setImmediate < "u" ? setImmediate : null;
    function Y(O) {
      for (var X = u(m); X !== null; ) {
        if (X.callback === null) o(m);
        else if (X.startTime <= O)
          o(m), X.sortIndex = X.expirationTime, l(g, X);
        else break;
        X = u(m);
      }
    }
    function tt(O) {
      if (j = !1, Y(O), !z)
        if (u(g) !== null)
          z = !0, nt || (nt = !0, vt());
        else {
          var X = u(m);
          X !== null && wt(tt, X.startTime - O);
        }
    }
    var nt = !1, Q = -1, K = 5, it = -1;
    function $() {
      return w ? !0 : !(i.unstable_now() - it < K);
    }
    function yt() {
      if (w = !1, nt) {
        var O = i.unstable_now();
        it = O;
        var X = !0;
        try {
          t: {
            z = !1, j && (j = !1, G(Q), Q = -1), _ = !0;
            var J = b;
            try {
              e: {
                for (Y(O), S = u(g); S !== null && !(S.expirationTime > O && $()); ) {
                  var ut = S.callback;
                  if (typeof ut == "function") {
                    S.callback = null, b = S.priorityLevel;
                    var pt = ut(
                      S.expirationTime <= O
                    );
                    if (O = i.unstable_now(), typeof pt == "function") {
                      S.callback = pt, Y(O), X = !0;
                      break e;
                    }
                    S === u(g) && o(g), Y(O);
                  } else o(g);
                  S = u(g);
                }
                if (S !== null) X = !0;
                else {
                  var E = u(m);
                  E !== null && wt(
                    tt,
                    E.startTime - O
                  ), X = !1;
                }
              }
              break t;
            } finally {
              S = null, b = J, _ = !1;
            }
            X = void 0;
          }
        } finally {
          X ? vt() : nt = !1;
        }
      }
    }
    var vt;
    if (typeof H == "function")
      vt = function() {
        H(yt);
      };
    else if (typeof MessageChannel < "u") {
      var Pt = new MessageChannel(), qt = Pt.port2;
      Pt.port1.onmessage = yt, vt = function() {
        qt.postMessage(null);
      };
    } else
      vt = function() {
        L(yt, 0);
      };
    function wt(O, X) {
      Q = L(function() {
        O(i.unstable_now());
      }, X);
    }
    i.unstable_IdlePriority = 5, i.unstable_ImmediatePriority = 1, i.unstable_LowPriority = 4, i.unstable_NormalPriority = 3, i.unstable_Profiling = null, i.unstable_UserBlockingPriority = 2, i.unstable_cancelCallback = function(O) {
      O.callback = null;
    }, i.unstable_forceFrameRate = function(O) {
      0 > O || 125 < O ? console.error(
        "forceFrameRate takes a positive int between 0 and 125, forcing frame rates higher than 125 fps is not supported"
      ) : K = 0 < O ? Math.floor(1e3 / O) : 5;
    }, i.unstable_getCurrentPriorityLevel = function() {
      return b;
    }, i.unstable_next = function(O) {
      switch (b) {
        case 1:
        case 2:
        case 3:
          var X = 3;
          break;
        default:
          X = b;
      }
      var J = b;
      b = X;
      try {
        return O();
      } finally {
        b = J;
      }
    }, i.unstable_requestPaint = function() {
      w = !0;
    }, i.unstable_runWithPriority = function(O, X) {
      switch (O) {
        case 1:
        case 2:
        case 3:
        case 4:
        case 5:
          break;
        default:
          O = 3;
      }
      var J = b;
      b = O;
      try {
        return X();
      } finally {
        b = J;
      }
    }, i.unstable_scheduleCallback = function(O, X, J) {
      var ut = i.unstable_now();
      switch (typeof J == "object" && J !== null ? (J = J.delay, J = typeof J == "number" && 0 < J ? ut + J : ut) : J = ut, O) {
        case 1:
          var pt = -1;
          break;
        case 2:
          pt = 250;
          break;
        case 5:
          pt = 1073741823;
          break;
        case 4:
          pt = 1e4;
          break;
        default:
          pt = 5e3;
      }
      return pt = J + pt, O = {
        id: v++,
        callback: X,
        priorityLevel: O,
        startTime: J,
        expirationTime: pt,
        sortIndex: -1
      }, J > ut ? (O.sortIndex = J, l(m, O), u(g) === null && O === u(m) && (j ? (G(Q), Q = -1) : j = !0, wt(tt, J - ut))) : (O.sortIndex = pt, l(g, O), z || _ || (z = !0, nt || (nt = !0, vt()))), O;
    }, i.unstable_shouldYield = $, i.unstable_wrapCallback = function(O) {
      var X = b;
      return function() {
        var J = b;
        b = X;
        try {
          return O.apply(this, arguments);
        } finally {
          b = J;
        }
      };
    };
  })(Xr)), Xr;
}
var my;
function J1() {
  return my || (my = 1, Gr.exports = K1()), Gr.exports;
}
var Zr = { exports: {} }, le = {};
var yy;
function k1() {
  if (yy) return le;
  yy = 1;
  var i = _c();
  function l(g) {
    var m = "https://react.dev/errors/" + g;
    if (1 < arguments.length) {
      m += "?args[]=" + encodeURIComponent(arguments[1]);
      for (var v = 2; v < arguments.length; v++)
        m += "&args[]=" + encodeURIComponent(arguments[v]);
    }
    return "Minified React error #" + g + "; visit " + m + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  function u() {
  }
  var o = {
    d: {
      f: u,
      r: function() {
        throw Error(l(522));
      },
      D: u,
      C: u,
      L: u,
      m: u,
      X: u,
      S: u,
      M: u
    },
    p: 0,
    findDOMNode: null
  }, c = /* @__PURE__ */ Symbol.for("react.portal");
  function d(g, m, v) {
    var S = 3 < arguments.length && arguments[3] !== void 0 ? arguments[3] : null;
    return {
      $$typeof: c,
      key: S == null ? null : "" + S,
      children: g,
      containerInfo: m,
      implementation: v
    };
  }
  var h = i.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE;
  function y(g, m) {
    if (g === "font") return "";
    if (typeof m == "string")
      return m === "use-credentials" ? m : "";
  }
  return le.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE = o, le.createPortal = function(g, m) {
    var v = 2 < arguments.length && arguments[2] !== void 0 ? arguments[2] : null;
    if (!m || m.nodeType !== 1 && m.nodeType !== 9 && m.nodeType !== 11)
      throw Error(l(299));
    return d(g, m, null, v);
  }, le.flushSync = function(g) {
    var m = h.T, v = o.p;
    try {
      if (h.T = null, o.p = 2, g) return g();
    } finally {
      h.T = m, o.p = v, o.d.f();
    }
  }, le.preconnect = function(g, m) {
    typeof g == "string" && (m ? (m = m.crossOrigin, m = typeof m == "string" ? m === "use-credentials" ? m : "" : void 0) : m = null, o.d.C(g, m));
  }, le.prefetchDNS = function(g) {
    typeof g == "string" && o.d.D(g);
  }, le.preinit = function(g, m) {
    if (typeof g == "string" && m && typeof m.as == "string") {
      var v = m.as, S = y(v, m.crossOrigin), b = typeof m.integrity == "string" ? m.integrity : void 0, _ = typeof m.fetchPriority == "string" ? m.fetchPriority : void 0;
      v === "style" ? o.d.S(
        g,
        typeof m.precedence == "string" ? m.precedence : void 0,
        {
          crossOrigin: S,
          integrity: b,
          fetchPriority: _
        }
      ) : v === "script" && o.d.X(g, {
        crossOrigin: S,
        integrity: b,
        fetchPriority: _,
        nonce: typeof m.nonce == "string" ? m.nonce : void 0
      });
    }
  }, le.preinitModule = function(g, m) {
    if (typeof g == "string")
      if (typeof m == "object" && m !== null) {
        if (m.as == null || m.as === "script") {
          var v = y(
            m.as,
            m.crossOrigin
          );
          o.d.M(g, {
            crossOrigin: v,
            integrity: typeof m.integrity == "string" ? m.integrity : void 0,
            nonce: typeof m.nonce == "string" ? m.nonce : void 0
          });
        }
      } else m == null && o.d.M(g);
  }, le.preload = function(g, m) {
    if (typeof g == "string" && typeof m == "object" && m !== null && typeof m.as == "string") {
      var v = m.as, S = y(v, m.crossOrigin);
      o.d.L(g, v, {
        crossOrigin: S,
        integrity: typeof m.integrity == "string" ? m.integrity : void 0,
        nonce: typeof m.nonce == "string" ? m.nonce : void 0,
        type: typeof m.type == "string" ? m.type : void 0,
        fetchPriority: typeof m.fetchPriority == "string" ? m.fetchPriority : void 0,
        referrerPolicy: typeof m.referrerPolicy == "string" ? m.referrerPolicy : void 0,
        imageSrcSet: typeof m.imageSrcSet == "string" ? m.imageSrcSet : void 0,
        imageSizes: typeof m.imageSizes == "string" ? m.imageSizes : void 0,
        media: typeof m.media == "string" ? m.media : void 0
      });
    }
  }, le.preloadModule = function(g, m) {
    if (typeof g == "string")
      if (m) {
        var v = y(m.as, m.crossOrigin);
        o.d.m(g, {
          as: typeof m.as == "string" && m.as !== "script" ? m.as : void 0,
          crossOrigin: v,
          integrity: typeof m.integrity == "string" ? m.integrity : void 0
        });
      } else o.d.m(g);
  }, le.requestFormReset = function(g) {
    o.d.r(g);
  }, le.unstable_batchedUpdates = function(g, m) {
    return g(m);
  }, le.useFormState = function(g, m, v) {
    return h.H.useFormState(g, m, v);
  }, le.useFormStatus = function() {
    return h.H.useHostTransitionStatus();
  }, le.version = "19.2.8", le;
}
var py;
function F1() {
  if (py) return Zr.exports;
  py = 1;
  function i() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(i);
      } catch (l) {
        console.error(l);
      }
  }
  return i(), Zr.exports = k1(), Zr.exports;
}
var gy;
function W1() {
  if (gy) return ul;
  gy = 1;
  var i = J1(), l = _c(), u = F1();
  function o(t) {
    var e = "https://react.dev/errors/" + t;
    if (1 < arguments.length) {
      e += "?args[]=" + encodeURIComponent(arguments[1]);
      for (var n = 2; n < arguments.length; n++)
        e += "&args[]=" + encodeURIComponent(arguments[n]);
    }
    return "Minified React error #" + t + "; visit " + e + " for the full message or use the non-minified dev environment for full errors and additional helpful warnings.";
  }
  function c(t) {
    return !(!t || t.nodeType !== 1 && t.nodeType !== 9 && t.nodeType !== 11);
  }
  function d(t) {
    var e = t, n = t;
    if (t.alternate) for (; e.return; ) e = e.return;
    else {
      t = e;
      do
        e = t, (e.flags & 4098) !== 0 && (n = e.return), t = e.return;
      while (t);
    }
    return e.tag === 3 ? n : null;
  }
  function h(t) {
    if (t.tag === 13) {
      var e = t.memoizedState;
      if (e === null && (t = t.alternate, t !== null && (e = t.memoizedState)), e !== null) return e.dehydrated;
    }
    return null;
  }
  function y(t) {
    if (t.tag === 31) {
      var e = t.memoizedState;
      if (e === null && (t = t.alternate, t !== null && (e = t.memoizedState)), e !== null) return e.dehydrated;
    }
    return null;
  }
  function g(t) {
    if (d(t) !== t)
      throw Error(o(188));
  }
  function m(t) {
    var e = t.alternate;
    if (!e) {
      if (e = d(t), e === null) throw Error(o(188));
      return e !== t ? null : t;
    }
    for (var n = t, a = e; ; ) {
      var s = n.return;
      if (s === null) break;
      var r = s.alternate;
      if (r === null) {
        if (a = s.return, a !== null) {
          n = a;
          continue;
        }
        break;
      }
      if (s.child === r.child) {
        for (r = s.child; r; ) {
          if (r === n) return g(s), t;
          if (r === a) return g(s), e;
          r = r.sibling;
        }
        throw Error(o(188));
      }
      if (n.return !== a.return) n = s, a = r;
      else {
        for (var f = !1, p = s.child; p; ) {
          if (p === n) {
            f = !0, n = s, a = r;
            break;
          }
          if (p === a) {
            f = !0, a = s, n = r;
            break;
          }
          p = p.sibling;
        }
        if (!f) {
          for (p = r.child; p; ) {
            if (p === n) {
              f = !0, n = r, a = s;
              break;
            }
            if (p === a) {
              f = !0, a = r, n = s;
              break;
            }
            p = p.sibling;
          }
          if (!f) throw Error(o(189));
        }
      }
      if (n.alternate !== a) throw Error(o(190));
    }
    if (n.tag !== 3) throw Error(o(188));
    return n.stateNode.current === n ? t : e;
  }
  function v(t) {
    var e = t.tag;
    if (e === 5 || e === 26 || e === 27 || e === 6) return t;
    for (t = t.child; t !== null; ) {
      if (e = v(t), e !== null) return e;
      t = t.sibling;
    }
    return null;
  }
  var S = Object.assign, b = /* @__PURE__ */ Symbol.for("react.element"), _ = /* @__PURE__ */ Symbol.for("react.transitional.element"), z = /* @__PURE__ */ Symbol.for("react.portal"), j = /* @__PURE__ */ Symbol.for("react.fragment"), w = /* @__PURE__ */ Symbol.for("react.strict_mode"), L = /* @__PURE__ */ Symbol.for("react.profiler"), G = /* @__PURE__ */ Symbol.for("react.consumer"), H = /* @__PURE__ */ Symbol.for("react.context"), Y = /* @__PURE__ */ Symbol.for("react.forward_ref"), tt = /* @__PURE__ */ Symbol.for("react.suspense"), nt = /* @__PURE__ */ Symbol.for("react.suspense_list"), Q = /* @__PURE__ */ Symbol.for("react.memo"), K = /* @__PURE__ */ Symbol.for("react.lazy"), it = /* @__PURE__ */ Symbol.for("react.activity"), $ = /* @__PURE__ */ Symbol.for("react.memo_cache_sentinel"), yt = Symbol.iterator;
  function vt(t) {
    return t === null || typeof t != "object" ? null : (t = yt && t[yt] || t["@@iterator"], typeof t == "function" ? t : null);
  }
  var Pt = /* @__PURE__ */ Symbol.for("react.client.reference");
  function qt(t) {
    if (t == null) return null;
    if (typeof t == "function")
      return t.$$typeof === Pt ? null : t.displayName || t.name || null;
    if (typeof t == "string") return t;
    switch (t) {
      case j:
        return "Fragment";
      case L:
        return "Profiler";
      case w:
        return "StrictMode";
      case tt:
        return "Suspense";
      case nt:
        return "SuspenseList";
      case it:
        return "Activity";
    }
    if (typeof t == "object")
      switch (t.$$typeof) {
        case z:
          return "Portal";
        case H:
          return t.displayName || "Context";
        case G:
          return (t._context.displayName || "Context") + ".Consumer";
        case Y:
          var e = t.render;
          return t = t.displayName, t || (t = e.displayName || e.name || "", t = t !== "" ? "ForwardRef(" + t + ")" : "ForwardRef"), t;
        case Q:
          return e = t.displayName || null, e !== null ? e : qt(t.type) || "Memo";
        case K:
          e = t._payload, t = t._init;
          try {
            return qt(t(e));
          } catch {
          }
      }
    return null;
  }
  var wt = Array.isArray, O = l.__CLIENT_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, X = u.__DOM_INTERNALS_DO_NOT_USE_OR_WARN_USERS_THEY_CANNOT_UPGRADE, J = {
    pending: !1,
    data: null,
    method: null,
    action: null
  }, ut = [], pt = -1;
  function E(t) {
    return { current: t };
  }
  function N(t) {
    0 > pt || (t.current = ut[pt], ut[pt] = null, pt--);
  }
  function Z(t, e) {
    pt++, ut[pt] = t.current, t.current = e;
  }
  var W = E(null), lt = E(null), ct = E(null), At = E(null);
  function se(t, e) {
    switch (Z(ct, e), Z(lt, t), Z(W, null), e.nodeType) {
      case 9:
      case 11:
        t = (t = e.documentElement) && (t = t.namespaceURI) ? _m(t) : 0;
        break;
      default:
        if (t = e.tagName, e = e.namespaceURI)
          e = _m(e), t = Um(e, t);
        else
          switch (t) {
            case "svg":
              t = 1;
              break;
            case "math":
              t = 2;
              break;
            default:
              t = 0;
          }
    }
    N(W), Z(W, t);
  }
  function Lt() {
    N(W), N(lt), N(ct);
  }
  function da(t) {
    t.memoizedState !== null && Z(At, t);
    var e = W.current, n = Um(e, t.type);
    e !== n && (Z(lt, t), Z(W, n));
  }
  function xl(t) {
    lt.current === t && (N(W), N(lt)), At.current === t && (N(At), nl._currentValue = J);
  }
  var Tu, of;
  function Fn(t) {
    if (Tu === void 0)
      try {
        throw Error();
      } catch (n) {
        var e = n.stack.trim().match(/\n( *(at )?)/);
        Tu = e && e[1] || "", of = -1 < n.stack.indexOf(`
    at`) ? " (<anonymous>)" : -1 < n.stack.indexOf("@") ? "@unknown:0:0" : "";
      }
    return `
` + Tu + t + of;
  }
  var bu = !1;
  function Au(t, e) {
    if (!t || bu) return "";
    bu = !0;
    var n = Error.prepareStackTrace;
    Error.prepareStackTrace = void 0;
    try {
      var a = {
        DetermineComponentFrameRoot: function() {
          try {
            if (e) {
              var B = function() {
                throw Error();
              };
              if (Object.defineProperty(B.prototype, "props", {
                set: function() {
                  throw Error();
                }
              }), typeof Reflect == "object" && Reflect.construct) {
                try {
                  Reflect.construct(B, []);
                } catch (R) {
                  var C = R;
                }
                Reflect.construct(t, [], B);
              } else {
                try {
                  B.call();
                } catch (R) {
                  C = R;
                }
                t.call(B.prototype);
              }
            } else {
              try {
                throw Error();
              } catch (R) {
                C = R;
              }
              (B = t()) && typeof B.catch == "function" && B.catch(function() {
              });
            }
          } catch (R) {
            if (R && C && typeof R.stack == "string")
              return [R.stack, C.stack];
          }
          return [null, null];
        }
      };
      a.DetermineComponentFrameRoot.displayName = "DetermineComponentFrameRoot";
      var s = Object.getOwnPropertyDescriptor(
        a.DetermineComponentFrameRoot,
        "name"
      );
      s && s.configurable && Object.defineProperty(
        a.DetermineComponentFrameRoot,
        "name",
        { value: "DetermineComponentFrameRoot" }
      );
      var r = a.DetermineComponentFrameRoot(), f = r[0], p = r[1];
      if (f && p) {
        var T = f.split(`
`), D = p.split(`
`);
        for (s = a = 0; a < T.length && !T[a].includes("DetermineComponentFrameRoot"); )
          a++;
        for (; s < D.length && !D[s].includes(
          "DetermineComponentFrameRoot"
        ); )
          s++;
        if (a === T.length || s === D.length)
          for (a = T.length - 1, s = D.length - 1; 1 <= a && 0 <= s && T[a] !== D[s]; )
            s--;
        for (; 1 <= a && 0 <= s; a--, s--)
          if (T[a] !== D[s]) {
            if (a !== 1 || s !== 1)
              do
                if (a--, s--, 0 > s || T[a] !== D[s]) {
                  var V = `
` + T[a].replace(" at new ", " at ");
                  return t.displayName && V.includes("<anonymous>") && (V = V.replace("<anonymous>", t.displayName)), V;
                }
              while (1 <= a && 0 <= s);
            break;
          }
      }
    } finally {
      bu = !1, Error.prepareStackTrace = n;
    }
    return (n = t ? t.displayName || t.name : "") ? Fn(n) : "";
  }
  function T0(t, e) {
    switch (t.tag) {
      case 26:
      case 27:
      case 5:
        return Fn(t.type);
      case 16:
        return Fn("Lazy");
      case 13:
        return t.child !== e && e !== null ? Fn("Suspense Fallback") : Fn("Suspense");
      case 19:
        return Fn("SuspenseList");
      case 0:
      case 15:
        return Au(t.type, !1);
      case 11:
        return Au(t.type.render, !1);
      case 1:
        return Au(t.type, !0);
      case 31:
        return Fn("Activity");
      default:
        return "";
    }
  }
  function rf(t) {
    try {
      var e = "", n = null;
      do
        e += T0(t, n), n = t, t = t.return;
      while (t);
      return e;
    } catch (a) {
      return `
Error generating stack: ` + a.message + `
` + a.stack;
    }
  }
  var Eu = Object.prototype.hasOwnProperty, xu = i.unstable_scheduleCallback, Mu = i.unstable_cancelCallback, b0 = i.unstable_shouldYield, A0 = i.unstable_requestPaint, ge = i.unstable_now, E0 = i.unstable_getCurrentPriorityLevel, cf = i.unstable_ImmediatePriority, ff = i.unstable_UserBlockingPriority, Ml = i.unstable_NormalPriority, x0 = i.unstable_LowPriority, hf = i.unstable_IdlePriority, M0 = i.log, D0 = i.unstable_setDisableYieldValue, ma = null, ve = null;
  function Tn(t) {
    if (typeof M0 == "function" && D0(t), ve && typeof ve.setStrictMode == "function")
      try {
        ve.setStrictMode(ma, t);
      } catch {
      }
  }
  var Se = Math.clz32 ? Math.clz32 : R0, C0 = Math.log, z0 = Math.LN2;
  function R0(t) {
    return t >>>= 0, t === 0 ? 32 : 31 - (C0(t) / z0 | 0) | 0;
  }
  var Dl = 256, Cl = 262144, zl = 4194304;
  function Wn(t) {
    var e = t & 42;
    if (e !== 0) return e;
    switch (t & -t) {
      case 1:
        return 1;
      case 2:
        return 2;
      case 4:
        return 4;
      case 8:
        return 8;
      case 16:
        return 16;
      case 32:
        return 32;
      case 64:
        return 64;
      case 128:
        return 128;
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
        return t & 261888;
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return t & 3932160;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        return t & 62914560;
      case 67108864:
        return 67108864;
      case 134217728:
        return 134217728;
      case 268435456:
        return 268435456;
      case 536870912:
        return 536870912;
      case 1073741824:
        return 0;
      default:
        return t;
    }
  }
  function Rl(t, e, n) {
    var a = t.pendingLanes;
    if (a === 0) return 0;
    var s = 0, r = t.suspendedLanes, f = t.pingedLanes;
    t = t.warmLanes;
    var p = a & 134217727;
    return p !== 0 ? (a = p & ~r, a !== 0 ? s = Wn(a) : (f &= p, f !== 0 ? s = Wn(f) : n || (n = p & ~t, n !== 0 && (s = Wn(n))))) : (p = a & ~r, p !== 0 ? s = Wn(p) : f !== 0 ? s = Wn(f) : n || (n = a & ~t, n !== 0 && (s = Wn(n)))), s === 0 ? 0 : e !== 0 && e !== s && (e & r) === 0 && (r = s & -s, n = e & -e, r >= n || r === 32 && (n & 4194048) !== 0) ? e : s;
  }
  function ya(t, e) {
    return (t.pendingLanes & ~(t.suspendedLanes & ~t.pingedLanes) & e) === 0;
  }
  function O0(t, e) {
    switch (t) {
      case 1:
      case 2:
      case 4:
      case 8:
      case 64:
        return e + 250;
      case 16:
      case 32:
      case 128:
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
        return e + 5e3;
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        return -1;
      case 67108864:
      case 134217728:
      case 268435456:
      case 536870912:
      case 1073741824:
        return -1;
      default:
        return -1;
    }
  }
  function df() {
    var t = zl;
    return zl <<= 1, (zl & 62914560) === 0 && (zl = 4194304), t;
  }
  function Du(t) {
    for (var e = [], n = 0; 31 > n; n++) e.push(t);
    return e;
  }
  function pa(t, e) {
    t.pendingLanes |= e, e !== 268435456 && (t.suspendedLanes = 0, t.pingedLanes = 0, t.warmLanes = 0);
  }
  function V0(t, e, n, a, s, r) {
    var f = t.pendingLanes;
    t.pendingLanes = n, t.suspendedLanes = 0, t.pingedLanes = 0, t.warmLanes = 0, t.expiredLanes &= n, t.entangledLanes &= n, t.errorRecoveryDisabledLanes &= n, t.shellSuspendCounter = 0;
    var p = t.entanglements, T = t.expirationTimes, D = t.hiddenUpdates;
    for (n = f & ~n; 0 < n; ) {
      var V = 31 - Se(n), B = 1 << V;
      p[V] = 0, T[V] = -1;
      var C = D[V];
      if (C !== null)
        for (D[V] = null, V = 0; V < C.length; V++) {
          var R = C[V];
          R !== null && (R.lane &= -536870913);
        }
      n &= ~B;
    }
    a !== 0 && mf(t, a, 0), r !== 0 && s === 0 && t.tag !== 0 && (t.suspendedLanes |= r & ~(f & ~e));
  }
  function mf(t, e, n) {
    t.pendingLanes |= e, t.suspendedLanes &= ~e;
    var a = 31 - Se(e);
    t.entangledLanes |= e, t.entanglements[a] = t.entanglements[a] | 1073741824 | n & 261930;
  }
  function yf(t, e) {
    var n = t.entangledLanes |= e;
    for (t = t.entanglements; n; ) {
      var a = 31 - Se(n), s = 1 << a;
      s & e | t[a] & e && (t[a] |= e), n &= ~s;
    }
  }
  function pf(t, e) {
    var n = e & -e;
    return n = (n & 42) !== 0 ? 1 : Cu(n), (n & (t.suspendedLanes | e)) !== 0 ? 0 : n;
  }
  function Cu(t) {
    switch (t) {
      case 2:
        t = 1;
        break;
      case 8:
        t = 4;
        break;
      case 32:
        t = 16;
        break;
      case 256:
      case 512:
      case 1024:
      case 2048:
      case 4096:
      case 8192:
      case 16384:
      case 32768:
      case 65536:
      case 131072:
      case 262144:
      case 524288:
      case 1048576:
      case 2097152:
      case 4194304:
      case 8388608:
      case 16777216:
      case 33554432:
        t = 128;
        break;
      case 268435456:
        t = 134217728;
        break;
      default:
        t = 0;
    }
    return t;
  }
  function zu(t) {
    return t &= -t, 2 < t ? 8 < t ? (t & 134217727) !== 0 ? 32 : 268435456 : 8 : 2;
  }
  function gf() {
    var t = X.p;
    return t !== 0 ? t : (t = window.event, t === void 0 ? 32 : ny(t.type));
  }
  function vf(t, e) {
    var n = X.p;
    try {
      return X.p = t, e();
    } finally {
      X.p = n;
    }
  }
  var bn = Math.random().toString(36).slice(2), $t = "__reactFiber$" + bn, ce = "__reactProps$" + bn, Ti = "__reactContainer$" + bn, Ru = "__reactEvents$" + bn, _0 = "__reactListeners$" + bn, U0 = "__reactHandles$" + bn, Sf = "__reactResources$" + bn, ga = "__reactMarker$" + bn;
  function Ou(t) {
    delete t[$t], delete t[ce], delete t[Ru], delete t[_0], delete t[U0];
  }
  function bi(t) {
    var e = t[$t];
    if (e) return e;
    for (var n = t.parentNode; n; ) {
      if (e = n[Ti] || n[$t]) {
        if (n = e.alternate, e.child !== null || n !== null && n.child !== null)
          for (t = Ym(t); t !== null; ) {
            if (n = t[$t]) return n;
            t = Ym(t);
          }
        return e;
      }
      t = n, n = t.parentNode;
    }
    return null;
  }
  function Ai(t) {
    if (t = t[$t] || t[Ti]) {
      var e = t.tag;
      if (e === 5 || e === 6 || e === 13 || e === 31 || e === 26 || e === 27 || e === 3)
        return t;
    }
    return null;
  }
  function va(t) {
    var e = t.tag;
    if (e === 5 || e === 26 || e === 27 || e === 6) return t.stateNode;
    throw Error(o(33));
  }
  function Ei(t) {
    var e = t[Sf];
    return e || (e = t[Sf] = { hoistableStyles: /* @__PURE__ */ new Map(), hoistableScripts: /* @__PURE__ */ new Map() }), e;
  }
  function Ft(t) {
    t[ga] = !0;
  }
  var Tf = /* @__PURE__ */ new Set(), bf = {};
  function Pn(t, e) {
    xi(t, e), xi(t + "Capture", e);
  }
  function xi(t, e) {
    for (bf[t] = e, t = 0; t < e.length; t++)
      Tf.add(e[t]);
  }
  var B0 = RegExp(
    "^[:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD][:A-Z_a-z\\u00C0-\\u00D6\\u00D8-\\u00F6\\u00F8-\\u02FF\\u0370-\\u037D\\u037F-\\u1FFF\\u200C-\\u200D\\u2070-\\u218F\\u2C00-\\u2FEF\\u3001-\\uD7FF\\uF900-\\uFDCF\\uFDF0-\\uFFFD\\-.0-9\\u00B7\\u0300-\\u036F\\u203F-\\u2040]*$"
  ), Af = {}, Ef = {};
  function N0(t) {
    return Eu.call(Ef, t) ? !0 : Eu.call(Af, t) ? !1 : B0.test(t) ? Ef[t] = !0 : (Af[t] = !0, !1);
  }
  function Ol(t, e, n) {
    if (N0(e))
      if (n === null) t.removeAttribute(e);
      else {
        switch (typeof n) {
          case "undefined":
          case "function":
          case "symbol":
            t.removeAttribute(e);
            return;
          case "boolean":
            var a = e.toLowerCase().slice(0, 5);
            if (a !== "data-" && a !== "aria-") {
              t.removeAttribute(e);
              return;
            }
        }
        t.setAttribute(e, "" + n);
      }
  }
  function Vl(t, e, n) {
    if (n === null) t.removeAttribute(e);
    else {
      switch (typeof n) {
        case "undefined":
        case "function":
        case "symbol":
        case "boolean":
          t.removeAttribute(e);
          return;
      }
      t.setAttribute(e, "" + n);
    }
  }
  function tn(t, e, n, a) {
    if (a === null) t.removeAttribute(n);
    else {
      switch (typeof a) {
        case "undefined":
        case "function":
        case "symbol":
        case "boolean":
          t.removeAttribute(n);
          return;
      }
      t.setAttributeNS(e, n, "" + a);
    }
  }
  function ze(t) {
    switch (typeof t) {
      case "bigint":
      case "boolean":
      case "number":
      case "string":
      case "undefined":
        return t;
      case "object":
        return t;
      default:
        return "";
    }
  }
  function xf(t) {
    var e = t.type;
    return (t = t.nodeName) && t.toLowerCase() === "input" && (e === "checkbox" || e === "radio");
  }
  function j0(t, e, n) {
    var a = Object.getOwnPropertyDescriptor(
      t.constructor.prototype,
      e
    );
    if (!t.hasOwnProperty(e) && typeof a < "u" && typeof a.get == "function" && typeof a.set == "function") {
      var s = a.get, r = a.set;
      return Object.defineProperty(t, e, {
        configurable: !0,
        get: function() {
          return s.call(this);
        },
        set: function(f) {
          n = "" + f, r.call(this, f);
        }
      }), Object.defineProperty(t, e, {
        enumerable: a.enumerable
      }), {
        getValue: function() {
          return n;
        },
        setValue: function(f) {
          n = "" + f;
        },
        stopTracking: function() {
          t._valueTracker = null, delete t[e];
        }
      };
    }
  }
  function Vu(t) {
    if (!t._valueTracker) {
      var e = xf(t) ? "checked" : "value";
      t._valueTracker = j0(
        t,
        e,
        "" + t[e]
      );
    }
  }
  function Mf(t) {
    if (!t) return !1;
    var e = t._valueTracker;
    if (!e) return !0;
    var n = e.getValue(), a = "";
    return t && (a = xf(t) ? t.checked ? "true" : "false" : t.value), t = a, t !== n ? (e.setValue(t), !0) : !1;
  }
  function _l(t) {
    if (t = t || (typeof document < "u" ? document : void 0), typeof t > "u") return null;
    try {
      return t.activeElement || t.body;
    } catch {
      return t.body;
    }
  }
  var w0 = /[\n"\\]/g;
  function Re(t) {
    return t.replace(
      w0,
      function(e) {
        return "\\" + e.charCodeAt(0).toString(16) + " ";
      }
    );
  }
  function _u(t, e, n, a, s, r, f, p) {
    t.name = "", f != null && typeof f != "function" && typeof f != "symbol" && typeof f != "boolean" ? t.type = f : t.removeAttribute("type"), e != null ? f === "number" ? (e === 0 && t.value === "" || t.value != e) && (t.value = "" + ze(e)) : t.value !== "" + ze(e) && (t.value = "" + ze(e)) : f !== "submit" && f !== "reset" || t.removeAttribute("value"), e != null ? Uu(t, f, ze(e)) : n != null ? Uu(t, f, ze(n)) : a != null && t.removeAttribute("value"), s == null && r != null && (t.defaultChecked = !!r), s != null && (t.checked = s && typeof s != "function" && typeof s != "symbol"), p != null && typeof p != "function" && typeof p != "symbol" && typeof p != "boolean" ? t.name = "" + ze(p) : t.removeAttribute("name");
  }
  function Df(t, e, n, a, s, r, f, p) {
    if (r != null && typeof r != "function" && typeof r != "symbol" && typeof r != "boolean" && (t.type = r), e != null || n != null) {
      if (!(r !== "submit" && r !== "reset" || e != null)) {
        Vu(t);
        return;
      }
      n = n != null ? "" + ze(n) : "", e = e != null ? "" + ze(e) : n, p || e === t.value || (t.value = e), t.defaultValue = e;
    }
    a = a ?? s, a = typeof a != "function" && typeof a != "symbol" && !!a, t.checked = p ? t.checked : !!a, t.defaultChecked = !!a, f != null && typeof f != "function" && typeof f != "symbol" && typeof f != "boolean" && (t.name = f), Vu(t);
  }
  function Uu(t, e, n) {
    e === "number" && _l(t.ownerDocument) === t || t.defaultValue === "" + n || (t.defaultValue = "" + n);
  }
  function Mi(t, e, n, a) {
    if (t = t.options, e) {
      e = {};
      for (var s = 0; s < n.length; s++)
        e["$" + n[s]] = !0;
      for (n = 0; n < t.length; n++)
        s = e.hasOwnProperty("$" + t[n].value), t[n].selected !== s && (t[n].selected = s), s && a && (t[n].defaultSelected = !0);
    } else {
      for (n = "" + ze(n), e = null, s = 0; s < t.length; s++) {
        if (t[s].value === n) {
          t[s].selected = !0, a && (t[s].defaultSelected = !0);
          return;
        }
        e !== null || t[s].disabled || (e = t[s]);
      }
      e !== null && (e.selected = !0);
    }
  }
  function Cf(t, e, n) {
    if (e != null && (e = "" + ze(e), e !== t.value && (t.value = e), n == null)) {
      t.defaultValue !== e && (t.defaultValue = e);
      return;
    }
    t.defaultValue = n != null ? "" + ze(n) : "";
  }
  function zf(t, e, n, a) {
    if (e == null) {
      if (a != null) {
        if (n != null) throw Error(o(92));
        if (wt(a)) {
          if (1 < a.length) throw Error(o(93));
          a = a[0];
        }
        n = a;
      }
      n == null && (n = ""), e = n;
    }
    n = ze(e), t.defaultValue = n, a = t.textContent, a === n && a !== "" && a !== null && (t.value = a), Vu(t);
  }
  function Di(t, e) {
    if (e) {
      var n = t.firstChild;
      if (n && n === t.lastChild && n.nodeType === 3) {
        n.nodeValue = e;
        return;
      }
    }
    t.textContent = e;
  }
  var L0 = new Set(
    "animationIterationCount aspectRatio borderImageOutset borderImageSlice borderImageWidth boxFlex boxFlexGroup boxOrdinalGroup columnCount columns flex flexGrow flexPositive flexShrink flexNegative flexOrder gridArea gridRow gridRowEnd gridRowSpan gridRowStart gridColumn gridColumnEnd gridColumnSpan gridColumnStart fontWeight lineClamp lineHeight opacity order orphans scale tabSize widows zIndex zoom fillOpacity floodOpacity stopOpacity strokeDasharray strokeDashoffset strokeMiterlimit strokeOpacity strokeWidth MozAnimationIterationCount MozBoxFlex MozBoxFlexGroup MozLineClamp msAnimationIterationCount msFlex msZoom msFlexGrow msFlexNegative msFlexOrder msFlexPositive msFlexShrink msGridColumn msGridColumnSpan msGridRow msGridRowSpan WebkitAnimationIterationCount WebkitBoxFlex WebKitBoxFlexGroup WebkitBoxOrdinalGroup WebkitColumnCount WebkitColumns WebkitFlex WebkitFlexGrow WebkitFlexPositive WebkitFlexShrink WebkitLineClamp".split(
      " "
    )
  );
  function Rf(t, e, n) {
    var a = e.indexOf("--") === 0;
    n == null || typeof n == "boolean" || n === "" ? a ? t.setProperty(e, "") : e === "float" ? t.cssFloat = "" : t[e] = "" : a ? t.setProperty(e, n) : typeof n != "number" || n === 0 || L0.has(e) ? e === "float" ? t.cssFloat = n : t[e] = ("" + n).trim() : t[e] = n + "px";
  }
  function Of(t, e, n) {
    if (e != null && typeof e != "object")
      throw Error(o(62));
    if (t = t.style, n != null) {
      for (var a in n)
        !n.hasOwnProperty(a) || e != null && e.hasOwnProperty(a) || (a.indexOf("--") === 0 ? t.setProperty(a, "") : a === "float" ? t.cssFloat = "" : t[a] = "");
      for (var s in e)
        a = e[s], e.hasOwnProperty(s) && n[s] !== a && Rf(t, s, a);
    } else
      for (var r in e)
        e.hasOwnProperty(r) && Rf(t, r, e[r]);
  }
  function Bu(t) {
    if (t.indexOf("-") === -1) return !1;
    switch (t) {
      case "annotation-xml":
      case "color-profile":
      case "font-face":
      case "font-face-src":
      case "font-face-uri":
      case "font-face-format":
      case "font-face-name":
      case "missing-glyph":
        return !1;
      default:
        return !0;
    }
  }
  var H0 = /* @__PURE__ */ new Map([
    ["acceptCharset", "accept-charset"],
    ["htmlFor", "for"],
    ["httpEquiv", "http-equiv"],
    ["crossOrigin", "crossorigin"],
    ["accentHeight", "accent-height"],
    ["alignmentBaseline", "alignment-baseline"],
    ["arabicForm", "arabic-form"],
    ["baselineShift", "baseline-shift"],
    ["capHeight", "cap-height"],
    ["clipPath", "clip-path"],
    ["clipRule", "clip-rule"],
    ["colorInterpolation", "color-interpolation"],
    ["colorInterpolationFilters", "color-interpolation-filters"],
    ["colorProfile", "color-profile"],
    ["colorRendering", "color-rendering"],
    ["dominantBaseline", "dominant-baseline"],
    ["enableBackground", "enable-background"],
    ["fillOpacity", "fill-opacity"],
    ["fillRule", "fill-rule"],
    ["floodColor", "flood-color"],
    ["floodOpacity", "flood-opacity"],
    ["fontFamily", "font-family"],
    ["fontSize", "font-size"],
    ["fontSizeAdjust", "font-size-adjust"],
    ["fontStretch", "font-stretch"],
    ["fontStyle", "font-style"],
    ["fontVariant", "font-variant"],
    ["fontWeight", "font-weight"],
    ["glyphName", "glyph-name"],
    ["glyphOrientationHorizontal", "glyph-orientation-horizontal"],
    ["glyphOrientationVertical", "glyph-orientation-vertical"],
    ["horizAdvX", "horiz-adv-x"],
    ["horizOriginX", "horiz-origin-x"],
    ["imageRendering", "image-rendering"],
    ["letterSpacing", "letter-spacing"],
    ["lightingColor", "lighting-color"],
    ["markerEnd", "marker-end"],
    ["markerMid", "marker-mid"],
    ["markerStart", "marker-start"],
    ["overlinePosition", "overline-position"],
    ["overlineThickness", "overline-thickness"],
    ["paintOrder", "paint-order"],
    ["panose-1", "panose-1"],
    ["pointerEvents", "pointer-events"],
    ["renderingIntent", "rendering-intent"],
    ["shapeRendering", "shape-rendering"],
    ["stopColor", "stop-color"],
    ["stopOpacity", "stop-opacity"],
    ["strikethroughPosition", "strikethrough-position"],
    ["strikethroughThickness", "strikethrough-thickness"],
    ["strokeDasharray", "stroke-dasharray"],
    ["strokeDashoffset", "stroke-dashoffset"],
    ["strokeLinecap", "stroke-linecap"],
    ["strokeLinejoin", "stroke-linejoin"],
    ["strokeMiterlimit", "stroke-miterlimit"],
    ["strokeOpacity", "stroke-opacity"],
    ["strokeWidth", "stroke-width"],
    ["textAnchor", "text-anchor"],
    ["textDecoration", "text-decoration"],
    ["textRendering", "text-rendering"],
    ["transformOrigin", "transform-origin"],
    ["underlinePosition", "underline-position"],
    ["underlineThickness", "underline-thickness"],
    ["unicodeBidi", "unicode-bidi"],
    ["unicodeRange", "unicode-range"],
    ["unitsPerEm", "units-per-em"],
    ["vAlphabetic", "v-alphabetic"],
    ["vHanging", "v-hanging"],
    ["vIdeographic", "v-ideographic"],
    ["vMathematical", "v-mathematical"],
    ["vectorEffect", "vector-effect"],
    ["vertAdvY", "vert-adv-y"],
    ["vertOriginX", "vert-origin-x"],
    ["vertOriginY", "vert-origin-y"],
    ["wordSpacing", "word-spacing"],
    ["writingMode", "writing-mode"],
    ["xmlnsXlink", "xmlns:xlink"],
    ["xHeight", "x-height"]
  ]), Y0 = /^[\u0000-\u001F ]*j[\r\n\t]*a[\r\n\t]*v[\r\n\t]*a[\r\n\t]*s[\r\n\t]*c[\r\n\t]*r[\r\n\t]*i[\r\n\t]*p[\r\n\t]*t[\r\n\t]*:/i;
  function Ul(t) {
    return Y0.test("" + t) ? "javascript:throw new Error('React has blocked a javascript: URL as a security precaution.')" : t;
  }
  function en() {
  }
  var Nu = null;
  function ju(t) {
    return t = t.target || t.srcElement || window, t.correspondingUseElement && (t = t.correspondingUseElement), t.nodeType === 3 ? t.parentNode : t;
  }
  var Ci = null, zi = null;
  function Vf(t) {
    var e = Ai(t);
    if (e && (t = e.stateNode)) {
      var n = t[ce] || null;
      t: switch (t = e.stateNode, e.type) {
        case "input":
          if (_u(
            t,
            n.value,
            n.defaultValue,
            n.defaultValue,
            n.checked,
            n.defaultChecked,
            n.type,
            n.name
          ), e = n.name, n.type === "radio" && e != null) {
            for (n = t; n.parentNode; ) n = n.parentNode;
            for (n = n.querySelectorAll(
              'input[name="' + Re(
                "" + e
              ) + '"][type="radio"]'
            ), e = 0; e < n.length; e++) {
              var a = n[e];
              if (a !== t && a.form === t.form) {
                var s = a[ce] || null;
                if (!s) throw Error(o(90));
                _u(
                  a,
                  s.value,
                  s.defaultValue,
                  s.defaultValue,
                  s.checked,
                  s.defaultChecked,
                  s.type,
                  s.name
                );
              }
            }
            for (e = 0; e < n.length; e++)
              a = n[e], a.form === t.form && Mf(a);
          }
          break t;
        case "textarea":
          Cf(t, n.value, n.defaultValue);
          break t;
        case "select":
          e = n.value, e != null && Mi(t, !!n.multiple, e, !1);
      }
    }
  }
  var wu = !1;
  function _f(t, e, n) {
    if (wu) return t(e, n);
    wu = !0;
    try {
      var a = t(e);
      return a;
    } finally {
      if (wu = !1, (Ci !== null || zi !== null) && (Ts(), Ci && (e = Ci, t = zi, zi = Ci = null, Vf(e), t)))
        for (e = 0; e < t.length; e++) Vf(t[e]);
    }
  }
  function Sa(t, e) {
    var n = t.stateNode;
    if (n === null) return null;
    var a = n[ce] || null;
    if (a === null) return null;
    n = a[e];
    t: switch (e) {
      case "onClick":
      case "onClickCapture":
      case "onDoubleClick":
      case "onDoubleClickCapture":
      case "onMouseDown":
      case "onMouseDownCapture":
      case "onMouseMove":
      case "onMouseMoveCapture":
      case "onMouseUp":
      case "onMouseUpCapture":
      case "onMouseEnter":
        (a = !a.disabled) || (t = t.type, a = !(t === "button" || t === "input" || t === "select" || t === "textarea")), t = !a;
        break t;
      default:
        t = !1;
    }
    if (t) return null;
    if (n && typeof n != "function")
      throw Error(
        o(231, e, typeof n)
      );
    return n;
  }
  var nn = !(typeof window > "u" || typeof window.document > "u" || typeof window.document.createElement > "u"), Lu = !1;
  if (nn)
    try {
      var Ta = {};
      Object.defineProperty(Ta, "passive", {
        get: function() {
          Lu = !0;
        }
      }), window.addEventListener("test", Ta, Ta), window.removeEventListener("test", Ta, Ta);
    } catch {
      Lu = !1;
    }
  var An = null, Hu = null, Bl = null;
  function Uf() {
    if (Bl) return Bl;
    var t, e = Hu, n = e.length, a, s = "value" in An ? An.value : An.textContent, r = s.length;
    for (t = 0; t < n && e[t] === s[t]; t++) ;
    var f = n - t;
    for (a = 1; a <= f && e[n - a] === s[r - a]; a++) ;
    return Bl = s.slice(t, 1 < a ? 1 - a : void 0);
  }
  function Nl(t) {
    var e = t.keyCode;
    return "charCode" in t ? (t = t.charCode, t === 0 && e === 13 && (t = 13)) : t = e, t === 10 && (t = 13), 32 <= t || t === 13 ? t : 0;
  }
  function jl() {
    return !0;
  }
  function Bf() {
    return !1;
  }
  function fe(t) {
    function e(n, a, s, r, f) {
      this._reactName = n, this._targetInst = s, this.type = a, this.nativeEvent = r, this.target = f, this.currentTarget = null;
      for (var p in t)
        t.hasOwnProperty(p) && (n = t[p], this[p] = n ? n(r) : r[p]);
      return this.isDefaultPrevented = (r.defaultPrevented != null ? r.defaultPrevented : r.returnValue === !1) ? jl : Bf, this.isPropagationStopped = Bf, this;
    }
    return S(e.prototype, {
      preventDefault: function() {
        this.defaultPrevented = !0;
        var n = this.nativeEvent;
        n && (n.preventDefault ? n.preventDefault() : typeof n.returnValue != "unknown" && (n.returnValue = !1), this.isDefaultPrevented = jl);
      },
      stopPropagation: function() {
        var n = this.nativeEvent;
        n && (n.stopPropagation ? n.stopPropagation() : typeof n.cancelBubble != "unknown" && (n.cancelBubble = !0), this.isPropagationStopped = jl);
      },
      persist: function() {
      },
      isPersistent: jl
    }), e;
  }
  var $n = {
    eventPhase: 0,
    bubbles: 0,
    cancelable: 0,
    timeStamp: function(t) {
      return t.timeStamp || Date.now();
    },
    defaultPrevented: 0,
    isTrusted: 0
  }, wl = fe($n), ba = S({}, $n, { view: 0, detail: 0 }), q0 = fe(ba), Yu, qu, Aa, Ll = S({}, ba, {
    screenX: 0,
    screenY: 0,
    clientX: 0,
    clientY: 0,
    pageX: 0,
    pageY: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    getModifierState: Xu,
    button: 0,
    buttons: 0,
    relatedTarget: function(t) {
      return t.relatedTarget === void 0 ? t.fromElement === t.srcElement ? t.toElement : t.fromElement : t.relatedTarget;
    },
    movementX: function(t) {
      return "movementX" in t ? t.movementX : (t !== Aa && (Aa && t.type === "mousemove" ? (Yu = t.screenX - Aa.screenX, qu = t.screenY - Aa.screenY) : qu = Yu = 0, Aa = t), Yu);
    },
    movementY: function(t) {
      return "movementY" in t ? t.movementY : qu;
    }
  }), Nf = fe(Ll), G0 = S({}, Ll, { dataTransfer: 0 }), X0 = fe(G0), Z0 = S({}, ba, { relatedTarget: 0 }), Gu = fe(Z0), Q0 = S({}, $n, {
    animationName: 0,
    elapsedTime: 0,
    pseudoElement: 0
  }), K0 = fe(Q0), J0 = S({}, $n, {
    clipboardData: function(t) {
      return "clipboardData" in t ? t.clipboardData : window.clipboardData;
    }
  }), k0 = fe(J0), F0 = S({}, $n, { data: 0 }), jf = fe(F0), W0 = {
    Esc: "Escape",
    Spacebar: " ",
    Left: "ArrowLeft",
    Up: "ArrowUp",
    Right: "ArrowRight",
    Down: "ArrowDown",
    Del: "Delete",
    Win: "OS",
    Menu: "ContextMenu",
    Apps: "ContextMenu",
    Scroll: "ScrollLock",
    MozPrintableKey: "Unidentified"
  }, P0 = {
    8: "Backspace",
    9: "Tab",
    12: "Clear",
    13: "Enter",
    16: "Shift",
    17: "Control",
    18: "Alt",
    19: "Pause",
    20: "CapsLock",
    27: "Escape",
    32: " ",
    33: "PageUp",
    34: "PageDown",
    35: "End",
    36: "Home",
    37: "ArrowLeft",
    38: "ArrowUp",
    39: "ArrowRight",
    40: "ArrowDown",
    45: "Insert",
    46: "Delete",
    112: "F1",
    113: "F2",
    114: "F3",
    115: "F4",
    116: "F5",
    117: "F6",
    118: "F7",
    119: "F8",
    120: "F9",
    121: "F10",
    122: "F11",
    123: "F12",
    144: "NumLock",
    145: "ScrollLock",
    224: "Meta"
  }, $0 = {
    Alt: "altKey",
    Control: "ctrlKey",
    Meta: "metaKey",
    Shift: "shiftKey"
  };
  function I0(t) {
    var e = this.nativeEvent;
    return e.getModifierState ? e.getModifierState(t) : (t = $0[t]) ? !!e[t] : !1;
  }
  function Xu() {
    return I0;
  }
  var tv = S({}, ba, {
    key: function(t) {
      if (t.key) {
        var e = W0[t.key] || t.key;
        if (e !== "Unidentified") return e;
      }
      return t.type === "keypress" ? (t = Nl(t), t === 13 ? "Enter" : String.fromCharCode(t)) : t.type === "keydown" || t.type === "keyup" ? P0[t.keyCode] || "Unidentified" : "";
    },
    code: 0,
    location: 0,
    ctrlKey: 0,
    shiftKey: 0,
    altKey: 0,
    metaKey: 0,
    repeat: 0,
    locale: 0,
    getModifierState: Xu,
    charCode: function(t) {
      return t.type === "keypress" ? Nl(t) : 0;
    },
    keyCode: function(t) {
      return t.type === "keydown" || t.type === "keyup" ? t.keyCode : 0;
    },
    which: function(t) {
      return t.type === "keypress" ? Nl(t) : t.type === "keydown" || t.type === "keyup" ? t.keyCode : 0;
    }
  }), ev = fe(tv), nv = S({}, Ll, {
    pointerId: 0,
    width: 0,
    height: 0,
    pressure: 0,
    tangentialPressure: 0,
    tiltX: 0,
    tiltY: 0,
    twist: 0,
    pointerType: 0,
    isPrimary: 0
  }), wf = fe(nv), iv = S({}, ba, {
    touches: 0,
    targetTouches: 0,
    changedTouches: 0,
    altKey: 0,
    metaKey: 0,
    ctrlKey: 0,
    shiftKey: 0,
    getModifierState: Xu
  }), av = fe(iv), lv = S({}, $n, {
    propertyName: 0,
    elapsedTime: 0,
    pseudoElement: 0
  }), sv = fe(lv), uv = S({}, Ll, {
    deltaX: function(t) {
      return "deltaX" in t ? t.deltaX : "wheelDeltaX" in t ? -t.wheelDeltaX : 0;
    },
    deltaY: function(t) {
      return "deltaY" in t ? t.deltaY : "wheelDeltaY" in t ? -t.wheelDeltaY : "wheelDelta" in t ? -t.wheelDelta : 0;
    },
    deltaZ: 0,
    deltaMode: 0
  }), ov = fe(uv), rv = S({}, $n, {
    newState: 0,
    oldState: 0
  }), cv = fe(rv), fv = [9, 13, 27, 32], Zu = nn && "CompositionEvent" in window, Ea = null;
  nn && "documentMode" in document && (Ea = document.documentMode);
  var hv = nn && "TextEvent" in window && !Ea, Lf = nn && (!Zu || Ea && 8 < Ea && 11 >= Ea), Hf = " ", Yf = !1;
  function qf(t, e) {
    switch (t) {
      case "keyup":
        return fv.indexOf(e.keyCode) !== -1;
      case "keydown":
        return e.keyCode !== 229;
      case "keypress":
      case "mousedown":
      case "focusout":
        return !0;
      default:
        return !1;
    }
  }
  function Gf(t) {
    return t = t.detail, typeof t == "object" && "data" in t ? t.data : null;
  }
  var Ri = !1;
  function dv(t, e) {
    switch (t) {
      case "compositionend":
        return Gf(e);
      case "keypress":
        return e.which !== 32 ? null : (Yf = !0, Hf);
      case "textInput":
        return t = e.data, t === Hf && Yf ? null : t;
      default:
        return null;
    }
  }
  function mv(t, e) {
    if (Ri)
      return t === "compositionend" || !Zu && qf(t, e) ? (t = Uf(), Bl = Hu = An = null, Ri = !1, t) : null;
    switch (t) {
      case "paste":
        return null;
      case "keypress":
        if (!(e.ctrlKey || e.altKey || e.metaKey) || e.ctrlKey && e.altKey) {
          if (e.char && 1 < e.char.length)
            return e.char;
          if (e.which) return String.fromCharCode(e.which);
        }
        return null;
      case "compositionend":
        return Lf && e.locale !== "ko" ? null : e.data;
      default:
        return null;
    }
  }
  var yv = {
    color: !0,
    date: !0,
    datetime: !0,
    "datetime-local": !0,
    email: !0,
    month: !0,
    number: !0,
    password: !0,
    range: !0,
    search: !0,
    tel: !0,
    text: !0,
    time: !0,
    url: !0,
    week: !0
  };
  function Xf(t) {
    var e = t && t.nodeName && t.nodeName.toLowerCase();
    return e === "input" ? !!yv[t.type] : e === "textarea";
  }
  function Zf(t, e, n, a) {
    Ci ? zi ? zi.push(a) : zi = [a] : Ci = a, e = Cs(e, "onChange"), 0 < e.length && (n = new wl(
      "onChange",
      "change",
      null,
      n,
      a
    ), t.push({ event: n, listeners: e }));
  }
  var xa = null, Ma = null;
  function pv(t) {
    Dm(t, 0);
  }
  function Hl(t) {
    var e = va(t);
    if (Mf(e)) return t;
  }
  function Qf(t, e) {
    if (t === "change") return e;
  }
  var Kf = !1;
  if (nn) {
    var Qu;
    if (nn) {
      var Ku = "oninput" in document;
      if (!Ku) {
        var Jf = document.createElement("div");
        Jf.setAttribute("oninput", "return;"), Ku = typeof Jf.oninput == "function";
      }
      Qu = Ku;
    } else Qu = !1;
    Kf = Qu && (!document.documentMode || 9 < document.documentMode);
  }
  function kf() {
    xa && (xa.detachEvent("onpropertychange", Ff), Ma = xa = null);
  }
  function Ff(t) {
    if (t.propertyName === "value" && Hl(Ma)) {
      var e = [];
      Zf(
        e,
        Ma,
        t,
        ju(t)
      ), _f(pv, e);
    }
  }
  function gv(t, e, n) {
    t === "focusin" ? (kf(), xa = e, Ma = n, xa.attachEvent("onpropertychange", Ff)) : t === "focusout" && kf();
  }
  function vv(t) {
    if (t === "selectionchange" || t === "keyup" || t === "keydown")
      return Hl(Ma);
  }
  function Sv(t, e) {
    if (t === "click") return Hl(e);
  }
  function Tv(t, e) {
    if (t === "input" || t === "change")
      return Hl(e);
  }
  function bv(t, e) {
    return t === e && (t !== 0 || 1 / t === 1 / e) || t !== t && e !== e;
  }
  var Te = typeof Object.is == "function" ? Object.is : bv;
  function Da(t, e) {
    if (Te(t, e)) return !0;
    if (typeof t != "object" || t === null || typeof e != "object" || e === null)
      return !1;
    var n = Object.keys(t), a = Object.keys(e);
    if (n.length !== a.length) return !1;
    for (a = 0; a < n.length; a++) {
      var s = n[a];
      if (!Eu.call(e, s) || !Te(t[s], e[s]))
        return !1;
    }
    return !0;
  }
  function Wf(t) {
    for (; t && t.firstChild; ) t = t.firstChild;
    return t;
  }
  function Pf(t, e) {
    var n = Wf(t);
    t = 0;
    for (var a; n; ) {
      if (n.nodeType === 3) {
        if (a = t + n.textContent.length, t <= e && a >= e)
          return { node: n, offset: e - t };
        t = a;
      }
      t: {
        for (; n; ) {
          if (n.nextSibling) {
            n = n.nextSibling;
            break t;
          }
          n = n.parentNode;
        }
        n = void 0;
      }
      n = Wf(n);
    }
  }
  function $f(t, e) {
    return t && e ? t === e ? !0 : t && t.nodeType === 3 ? !1 : e && e.nodeType === 3 ? $f(t, e.parentNode) : "contains" in t ? t.contains(e) : t.compareDocumentPosition ? !!(t.compareDocumentPosition(e) & 16) : !1 : !1;
  }
  function If(t) {
    t = t != null && t.ownerDocument != null && t.ownerDocument.defaultView != null ? t.ownerDocument.defaultView : window;
    for (var e = _l(t.document); e instanceof t.HTMLIFrameElement; ) {
      try {
        var n = typeof e.contentWindow.location.href == "string";
      } catch {
        n = !1;
      }
      if (n) t = e.contentWindow;
      else break;
      e = _l(t.document);
    }
    return e;
  }
  function Ju(t) {
    var e = t && t.nodeName && t.nodeName.toLowerCase();
    return e && (e === "input" && (t.type === "text" || t.type === "search" || t.type === "tel" || t.type === "url" || t.type === "password") || e === "textarea" || t.contentEditable === "true");
  }
  var Av = nn && "documentMode" in document && 11 >= document.documentMode, Oi = null, ku = null, Ca = null, Fu = !1;
  function th(t, e, n) {
    var a = n.window === n ? n.document : n.nodeType === 9 ? n : n.ownerDocument;
    Fu || Oi == null || Oi !== _l(a) || (a = Oi, "selectionStart" in a && Ju(a) ? a = { start: a.selectionStart, end: a.selectionEnd } : (a = (a.ownerDocument && a.ownerDocument.defaultView || window).getSelection(), a = {
      anchorNode: a.anchorNode,
      anchorOffset: a.anchorOffset,
      focusNode: a.focusNode,
      focusOffset: a.focusOffset
    }), Ca && Da(Ca, a) || (Ca = a, a = Cs(ku, "onSelect"), 0 < a.length && (e = new wl(
      "onSelect",
      "select",
      null,
      e,
      n
    ), t.push({ event: e, listeners: a }), e.target = Oi)));
  }
  function In(t, e) {
    var n = {};
    return n[t.toLowerCase()] = e.toLowerCase(), n["Webkit" + t] = "webkit" + e, n["Moz" + t] = "moz" + e, n;
  }
  var Vi = {
    animationend: In("Animation", "AnimationEnd"),
    animationiteration: In("Animation", "AnimationIteration"),
    animationstart: In("Animation", "AnimationStart"),
    transitionrun: In("Transition", "TransitionRun"),
    transitionstart: In("Transition", "TransitionStart"),
    transitioncancel: In("Transition", "TransitionCancel"),
    transitionend: In("Transition", "TransitionEnd")
  }, Wu = {}, eh = {};
  nn && (eh = document.createElement("div").style, "AnimationEvent" in window || (delete Vi.animationend.animation, delete Vi.animationiteration.animation, delete Vi.animationstart.animation), "TransitionEvent" in window || delete Vi.transitionend.transition);
  function ti(t) {
    if (Wu[t]) return Wu[t];
    if (!Vi[t]) return t;
    var e = Vi[t], n;
    for (n in e)
      if (e.hasOwnProperty(n) && n in eh)
        return Wu[t] = e[n];
    return t;
  }
  var nh = ti("animationend"), ih = ti("animationiteration"), ah = ti("animationstart"), Ev = ti("transitionrun"), xv = ti("transitionstart"), Mv = ti("transitioncancel"), lh = ti("transitionend"), sh = /* @__PURE__ */ new Map(), Pu = "abort auxClick beforeToggle cancel canPlay canPlayThrough click close contextMenu copy cut drag dragEnd dragEnter dragExit dragLeave dragOver dragStart drop durationChange emptied encrypted ended error gotPointerCapture input invalid keyDown keyPress keyUp load loadedData loadedMetadata loadStart lostPointerCapture mouseDown mouseMove mouseOut mouseOver mouseUp paste pause play playing pointerCancel pointerDown pointerMove pointerOut pointerOver pointerUp progress rateChange reset resize seeked seeking stalled submit suspend timeUpdate touchCancel touchEnd touchStart volumeChange scroll toggle touchMove waiting wheel".split(
    " "
  );
  Pu.push("scrollEnd");
  function Ye(t, e) {
    sh.set(t, e), Pn(e, [t]);
  }
  var Yl = typeof reportError == "function" ? reportError : function(t) {
    if (typeof window == "object" && typeof window.ErrorEvent == "function") {
      var e = new window.ErrorEvent("error", {
        bubbles: !0,
        cancelable: !0,
        message: typeof t == "object" && t !== null && typeof t.message == "string" ? String(t.message) : String(t),
        error: t
      });
      if (!window.dispatchEvent(e)) return;
    } else if (typeof process == "object" && typeof process.emit == "function") {
      process.emit("uncaughtException", t);
      return;
    }
    console.error(t);
  }, Oe = [], _i = 0, $u = 0;
  function ql() {
    for (var t = _i, e = $u = _i = 0; e < t; ) {
      var n = Oe[e];
      Oe[e++] = null;
      var a = Oe[e];
      Oe[e++] = null;
      var s = Oe[e];
      Oe[e++] = null;
      var r = Oe[e];
      if (Oe[e++] = null, a !== null && s !== null) {
        var f = a.pending;
        f === null ? s.next = s : (s.next = f.next, f.next = s), a.pending = s;
      }
      r !== 0 && uh(n, s, r);
    }
  }
  function Gl(t, e, n, a) {
    Oe[_i++] = t, Oe[_i++] = e, Oe[_i++] = n, Oe[_i++] = a, $u |= a, t.lanes |= a, t = t.alternate, t !== null && (t.lanes |= a);
  }
  function Iu(t, e, n, a) {
    return Gl(t, e, n, a), Xl(t);
  }
  function ei(t, e) {
    return Gl(t, null, null, e), Xl(t);
  }
  function uh(t, e, n) {
    t.lanes |= n;
    var a = t.alternate;
    a !== null && (a.lanes |= n);
    for (var s = !1, r = t.return; r !== null; )
      r.childLanes |= n, a = r.alternate, a !== null && (a.childLanes |= n), r.tag === 22 && (t = r.stateNode, t === null || t._visibility & 1 || (s = !0)), t = r, r = r.return;
    return t.tag === 3 ? (r = t.stateNode, s && e !== null && (s = 31 - Se(n), t = r.hiddenUpdates, a = t[s], a === null ? t[s] = [e] : a.push(e), e.lane = n | 536870912), r) : null;
  }
  function Xl(t) {
    if (50 < Fa)
      throw Fa = 0, rr = null, Error(o(185));
    for (var e = t.return; e !== null; )
      t = e, e = t.return;
    return t.tag === 3 ? t.stateNode : null;
  }
  var Ui = {};
  function Dv(t, e, n, a) {
    this.tag = t, this.key = n, this.sibling = this.child = this.return = this.stateNode = this.type = this.elementType = null, this.index = 0, this.refCleanup = this.ref = null, this.pendingProps = e, this.dependencies = this.memoizedState = this.updateQueue = this.memoizedProps = null, this.mode = a, this.subtreeFlags = this.flags = 0, this.deletions = null, this.childLanes = this.lanes = 0, this.alternate = null;
  }
  function be(t, e, n, a) {
    return new Dv(t, e, n, a);
  }
  function to(t) {
    return t = t.prototype, !(!t || !t.isReactComponent);
  }
  function an(t, e) {
    var n = t.alternate;
    return n === null ? (n = be(
      t.tag,
      e,
      t.key,
      t.mode
    ), n.elementType = t.elementType, n.type = t.type, n.stateNode = t.stateNode, n.alternate = t, t.alternate = n) : (n.pendingProps = e, n.type = t.type, n.flags = 0, n.subtreeFlags = 0, n.deletions = null), n.flags = t.flags & 65011712, n.childLanes = t.childLanes, n.lanes = t.lanes, n.child = t.child, n.memoizedProps = t.memoizedProps, n.memoizedState = t.memoizedState, n.updateQueue = t.updateQueue, e = t.dependencies, n.dependencies = e === null ? null : { lanes: e.lanes, firstContext: e.firstContext }, n.sibling = t.sibling, n.index = t.index, n.ref = t.ref, n.refCleanup = t.refCleanup, n;
  }
  function oh(t, e) {
    t.flags &= 65011714;
    var n = t.alternate;
    return n === null ? (t.childLanes = 0, t.lanes = e, t.child = null, t.subtreeFlags = 0, t.memoizedProps = null, t.memoizedState = null, t.updateQueue = null, t.dependencies = null, t.stateNode = null) : (t.childLanes = n.childLanes, t.lanes = n.lanes, t.child = n.child, t.subtreeFlags = 0, t.deletions = null, t.memoizedProps = n.memoizedProps, t.memoizedState = n.memoizedState, t.updateQueue = n.updateQueue, t.type = n.type, e = n.dependencies, t.dependencies = e === null ? null : {
      lanes: e.lanes,
      firstContext: e.firstContext
    }), t;
  }
  function Zl(t, e, n, a, s, r) {
    var f = 0;
    if (a = t, typeof t == "function") to(t) && (f = 1);
    else if (typeof t == "string")
      f = V1(
        t,
        n,
        W.current
      ) ? 26 : t === "html" || t === "head" || t === "body" ? 27 : 5;
    else
      t: switch (t) {
        case it:
          return t = be(31, n, e, s), t.elementType = it, t.lanes = r, t;
        case j:
          return ni(n.children, s, r, e);
        case w:
          f = 8, s |= 24;
          break;
        case L:
          return t = be(12, n, e, s | 2), t.elementType = L, t.lanes = r, t;
        case tt:
          return t = be(13, n, e, s), t.elementType = tt, t.lanes = r, t;
        case nt:
          return t = be(19, n, e, s), t.elementType = nt, t.lanes = r, t;
        default:
          if (typeof t == "object" && t !== null)
            switch (t.$$typeof) {
              case H:
                f = 10;
                break t;
              case G:
                f = 9;
                break t;
              case Y:
                f = 11;
                break t;
              case Q:
                f = 14;
                break t;
              case K:
                f = 16, a = null;
                break t;
            }
          f = 29, n = Error(
            o(130, t === null ? "null" : typeof t, "")
          ), a = null;
      }
    return e = be(f, n, e, s), e.elementType = t, e.type = a, e.lanes = r, e;
  }
  function ni(t, e, n, a) {
    return t = be(7, t, a, e), t.lanes = n, t;
  }
  function eo(t, e, n) {
    return t = be(6, t, null, e), t.lanes = n, t;
  }
  function rh(t) {
    var e = be(18, null, null, 0);
    return e.stateNode = t, e;
  }
  function no(t, e, n) {
    return e = be(
      4,
      t.children !== null ? t.children : [],
      t.key,
      e
    ), e.lanes = n, e.stateNode = {
      containerInfo: t.containerInfo,
      pendingChildren: null,
      implementation: t.implementation
    }, e;
  }
  var ch = /* @__PURE__ */ new WeakMap();
  function Ve(t, e) {
    if (typeof t == "object" && t !== null) {
      var n = ch.get(t);
      return n !== void 0 ? n : (e = {
        value: t,
        source: e,
        stack: rf(e)
      }, ch.set(t, e), e);
    }
    return {
      value: t,
      source: e,
      stack: rf(e)
    };
  }
  var Bi = [], Ni = 0, Ql = null, za = 0, _e = [], Ue = 0, En = null, Ke = 1, Je = "";
  function ln(t, e) {
    Bi[Ni++] = za, Bi[Ni++] = Ql, Ql = t, za = e;
  }
  function fh(t, e, n) {
    _e[Ue++] = Ke, _e[Ue++] = Je, _e[Ue++] = En, En = t;
    var a = Ke;
    t = Je;
    var s = 32 - Se(a) - 1;
    a &= ~(1 << s), n += 1;
    var r = 32 - Se(e) + s;
    if (30 < r) {
      var f = s - s % 5;
      r = (a & (1 << f) - 1).toString(32), a >>= f, s -= f, Ke = 1 << 32 - Se(e) + s | n << s | a, Je = r + t;
    } else
      Ke = 1 << r | n << s | a, Je = t;
  }
  function io(t) {
    t.return !== null && (ln(t, 1), fh(t, 1, 0));
  }
  function ao(t) {
    for (; t === Ql; )
      Ql = Bi[--Ni], Bi[Ni] = null, za = Bi[--Ni], Bi[Ni] = null;
    for (; t === En; )
      En = _e[--Ue], _e[Ue] = null, Je = _e[--Ue], _e[Ue] = null, Ke = _e[--Ue], _e[Ue] = null;
  }
  function hh(t, e) {
    _e[Ue++] = Ke, _e[Ue++] = Je, _e[Ue++] = En, Ke = e.id, Je = e.overflow, En = t;
  }
  var It = null, Vt = null, gt = !1, xn = null, Be = !1, lo = Error(o(519));
  function Mn(t) {
    var e = Error(
      o(
        418,
        1 < arguments.length && arguments[1] !== void 0 && arguments[1] ? "text" : "HTML",
        ""
      )
    );
    throw Ra(Ve(e, t)), lo;
  }
  function dh(t) {
    var e = t.stateNode, n = t.type, a = t.memoizedProps;
    switch (e[$t] = t, e[ce] = a, n) {
      case "dialog":
        ht("cancel", e), ht("close", e);
        break;
      case "iframe":
      case "object":
      case "embed":
        ht("load", e);
        break;
      case "video":
      case "audio":
        for (n = 0; n < Pa.length; n++)
          ht(Pa[n], e);
        break;
      case "source":
        ht("error", e);
        break;
      case "img":
      case "image":
      case "link":
        ht("error", e), ht("load", e);
        break;
      case "details":
        ht("toggle", e);
        break;
      case "input":
        ht("invalid", e), Df(
          e,
          a.value,
          a.defaultValue,
          a.checked,
          a.defaultChecked,
          a.type,
          a.name,
          !0
        );
        break;
      case "select":
        ht("invalid", e);
        break;
      case "textarea":
        ht("invalid", e), zf(e, a.value, a.defaultValue, a.children);
    }
    n = a.children, typeof n != "string" && typeof n != "number" && typeof n != "bigint" || e.textContent === "" + n || a.suppressHydrationWarning === !0 || Om(e.textContent, n) ? (a.popover != null && (ht("beforetoggle", e), ht("toggle", e)), a.onScroll != null && ht("scroll", e), a.onScrollEnd != null && ht("scrollend", e), a.onClick != null && (e.onclick = en), e = !0) : e = !1, e || Mn(t, !0);
  }
  function mh(t) {
    for (It = t.return; It; )
      switch (It.tag) {
        case 5:
        case 31:
        case 13:
          Be = !1;
          return;
        case 27:
        case 3:
          Be = !0;
          return;
        default:
          It = It.return;
      }
  }
  function ji(t) {
    if (t !== It) return !1;
    if (!gt) return mh(t), gt = !0, !1;
    var e = t.tag, n;
    if ((n = e !== 3 && e !== 27) && ((n = e === 5) && (n = t.type, n = !(n !== "form" && n !== "button") || xr(t.type, t.memoizedProps)), n = !n), n && Vt && Mn(t), mh(t), e === 13) {
      if (t = t.memoizedState, t = t !== null ? t.dehydrated : null, !t) throw Error(o(317));
      Vt = Hm(t);
    } else if (e === 31) {
      if (t = t.memoizedState, t = t !== null ? t.dehydrated : null, !t) throw Error(o(317));
      Vt = Hm(t);
    } else
      e === 27 ? (e = Vt, Hn(t.type) ? (t = Rr, Rr = null, Vt = t) : Vt = e) : Vt = It ? je(t.stateNode.nextSibling) : null;
    return !0;
  }
  function ii() {
    Vt = It = null, gt = !1;
  }
  function so() {
    var t = xn;
    return t !== null && (ye === null ? ye = t : ye.push.apply(
      ye,
      t
    ), xn = null), t;
  }
  function Ra(t) {
    xn === null ? xn = [t] : xn.push(t);
  }
  var uo = E(null), ai = null, sn = null;
  function Dn(t, e, n) {
    Z(uo, e._currentValue), e._currentValue = n;
  }
  function un(t) {
    t._currentValue = uo.current, N(uo);
  }
  function oo(t, e, n) {
    for (; t !== null; ) {
      var a = t.alternate;
      if ((t.childLanes & e) !== e ? (t.childLanes |= e, a !== null && (a.childLanes |= e)) : a !== null && (a.childLanes & e) !== e && (a.childLanes |= e), t === n) break;
      t = t.return;
    }
  }
  function ro(t, e, n, a) {
    var s = t.child;
    for (s !== null && (s.return = t); s !== null; ) {
      var r = s.dependencies;
      if (r !== null) {
        var f = s.child;
        r = r.firstContext;
        t: for (; r !== null; ) {
          var p = r;
          r = s;
          for (var T = 0; T < e.length; T++)
            if (p.context === e[T]) {
              r.lanes |= n, p = r.alternate, p !== null && (p.lanes |= n), oo(
                r.return,
                n,
                t
              ), a || (f = null);
              break t;
            }
          r = p.next;
        }
      } else if (s.tag === 18) {
        if (f = s.return, f === null) throw Error(o(341));
        f.lanes |= n, r = f.alternate, r !== null && (r.lanes |= n), oo(f, n, t), f = null;
      } else f = s.child;
      if (f !== null) f.return = s;
      else
        for (f = s; f !== null; ) {
          if (f === t) {
            f = null;
            break;
          }
          if (s = f.sibling, s !== null) {
            s.return = f.return, f = s;
            break;
          }
          f = f.return;
        }
      s = f;
    }
  }
  function wi(t, e, n, a) {
    t = null;
    for (var s = e, r = !1; s !== null; ) {
      if (!r) {
        if ((s.flags & 524288) !== 0) r = !0;
        else if ((s.flags & 262144) !== 0) break;
      }
      if (s.tag === 10) {
        var f = s.alternate;
        if (f === null) throw Error(o(387));
        if (f = f.memoizedProps, f !== null) {
          var p = s.type;
          Te(s.pendingProps.value, f.value) || (t !== null ? t.push(p) : t = [p]);
        }
      } else if (s === At.current) {
        if (f = s.alternate, f === null) throw Error(o(387));
        f.memoizedState.memoizedState !== s.memoizedState.memoizedState && (t !== null ? t.push(nl) : t = [nl]);
      }
      s = s.return;
    }
    t !== null && ro(
      e,
      t,
      n,
      a
    ), e.flags |= 262144;
  }
  function Kl(t) {
    for (t = t.firstContext; t !== null; ) {
      if (!Te(
        t.context._currentValue,
        t.memoizedValue
      ))
        return !0;
      t = t.next;
    }
    return !1;
  }
  function li(t) {
    ai = t, sn = null, t = t.dependencies, t !== null && (t.firstContext = null);
  }
  function te(t) {
    return yh(ai, t);
  }
  function Jl(t, e) {
    return ai === null && li(t), yh(t, e);
  }
  function yh(t, e) {
    var n = e._currentValue;
    if (e = { context: e, memoizedValue: n, next: null }, sn === null) {
      if (t === null) throw Error(o(308));
      sn = e, t.dependencies = { lanes: 0, firstContext: e }, t.flags |= 524288;
    } else sn = sn.next = e;
    return n;
  }
  var Cv = typeof AbortController < "u" ? AbortController : function() {
    var t = [], e = this.signal = {
      aborted: !1,
      addEventListener: function(n, a) {
        t.push(a);
      }
    };
    this.abort = function() {
      e.aborted = !0, t.forEach(function(n) {
        return n();
      });
    };
  }, zv = i.unstable_scheduleCallback, Rv = i.unstable_NormalPriority, Gt = {
    $$typeof: H,
    Consumer: null,
    Provider: null,
    _currentValue: null,
    _currentValue2: null,
    _threadCount: 0
  };
  function co() {
    return {
      controller: new Cv(),
      data: /* @__PURE__ */ new Map(),
      refCount: 0
    };
  }
  function Oa(t) {
    t.refCount--, t.refCount === 0 && zv(Rv, function() {
      t.controller.abort();
    });
  }
  var Va = null, fo = 0, Li = 0, Hi = null;
  function Ov(t, e) {
    if (Va === null) {
      var n = Va = [];
      fo = 0, Li = yr(), Hi = {
        status: "pending",
        value: void 0,
        then: function(a) {
          n.push(a);
        }
      };
    }
    return fo++, e.then(ph, ph), e;
  }
  function ph() {
    if (--fo === 0 && Va !== null) {
      Hi !== null && (Hi.status = "fulfilled");
      var t = Va;
      Va = null, Li = 0, Hi = null;
      for (var e = 0; e < t.length; e++) (0, t[e])();
    }
  }
  function Vv(t, e) {
    var n = [], a = {
      status: "pending",
      value: null,
      reason: null,
      then: function(s) {
        n.push(s);
      }
    };
    return t.then(
      function() {
        a.status = "fulfilled", a.value = e;
        for (var s = 0; s < n.length; s++) (0, n[s])(e);
      },
      function(s) {
        for (a.status = "rejected", a.reason = s, s = 0; s < n.length; s++)
          (0, n[s])(void 0);
      }
    ), a;
  }
  var gh = O.S;
  O.S = function(t, e) {
    tm = ge(), typeof e == "object" && e !== null && typeof e.then == "function" && Ov(t, e), gh !== null && gh(t, e);
  };
  var si = E(null);
  function ho() {
    var t = si.current;
    return t !== null ? t : zt.pooledCache;
  }
  function kl(t, e) {
    e === null ? Z(si, si.current) : Z(si, e.pool);
  }
  function vh() {
    var t = ho();
    return t === null ? null : { parent: Gt._currentValue, pool: t };
  }
  var Yi = Error(o(460)), mo = Error(o(474)), Fl = Error(o(542)), Wl = { then: function() {
  } };
  function Sh(t) {
    return t = t.status, t === "fulfilled" || t === "rejected";
  }
  function Th(t, e, n) {
    switch (n = t[n], n === void 0 ? t.push(e) : n !== e && (e.then(en, en), e = n), e.status) {
      case "fulfilled":
        return e.value;
      case "rejected":
        throw t = e.reason, Ah(t), t;
      default:
        if (typeof e.status == "string") e.then(en, en);
        else {
          if (t = zt, t !== null && 100 < t.shellSuspendCounter)
            throw Error(o(482));
          t = e, t.status = "pending", t.then(
            function(a) {
              if (e.status === "pending") {
                var s = e;
                s.status = "fulfilled", s.value = a;
              }
            },
            function(a) {
              if (e.status === "pending") {
                var s = e;
                s.status = "rejected", s.reason = a;
              }
            }
          );
        }
        switch (e.status) {
          case "fulfilled":
            return e.value;
          case "rejected":
            throw t = e.reason, Ah(t), t;
        }
        throw oi = e, Yi;
    }
  }
  function ui(t) {
    try {
      var e = t._init;
      return e(t._payload);
    } catch (n) {
      throw n !== null && typeof n == "object" && typeof n.then == "function" ? (oi = n, Yi) : n;
    }
  }
  var oi = null;
  function bh() {
    if (oi === null) throw Error(o(459));
    var t = oi;
    return oi = null, t;
  }
  function Ah(t) {
    if (t === Yi || t === Fl)
      throw Error(o(483));
  }
  var qi = null, _a = 0;
  function Pl(t) {
    var e = _a;
    return _a += 1, qi === null && (qi = []), Th(qi, t, e);
  }
  function Ua(t, e) {
    e = e.props.ref, t.ref = e !== void 0 ? e : null;
  }
  function $l(t, e) {
    throw e.$$typeof === b ? Error(o(525)) : (t = Object.prototype.toString.call(e), Error(
      o(
        31,
        t === "[object Object]" ? "object with keys {" + Object.keys(e).join(", ") + "}" : t
      )
    ));
  }
  function Eh(t) {
    function e(x, A) {
      if (t) {
        var M = x.deletions;
        M === null ? (x.deletions = [A], x.flags |= 16) : M.push(A);
      }
    }
    function n(x, A) {
      if (!t) return null;
      for (; A !== null; )
        e(x, A), A = A.sibling;
      return null;
    }
    function a(x) {
      for (var A = /* @__PURE__ */ new Map(); x !== null; )
        x.key !== null ? A.set(x.key, x) : A.set(x.index, x), x = x.sibling;
      return A;
    }
    function s(x, A) {
      return x = an(x, A), x.index = 0, x.sibling = null, x;
    }
    function r(x, A, M) {
      return x.index = M, t ? (M = x.alternate, M !== null ? (M = M.index, M < A ? (x.flags |= 67108866, A) : M) : (x.flags |= 67108866, A)) : (x.flags |= 1048576, A);
    }
    function f(x) {
      return t && x.alternate === null && (x.flags |= 67108866), x;
    }
    function p(x, A, M, U) {
      return A === null || A.tag !== 6 ? (A = eo(M, x.mode, U), A.return = x, A) : (A = s(A, M), A.return = x, A);
    }
    function T(x, A, M, U) {
      var I = M.type;
      return I === j ? V(
        x,
        A,
        M.props.children,
        U,
        M.key
      ) : A !== null && (A.elementType === I || typeof I == "object" && I !== null && I.$$typeof === K && ui(I) === A.type) ? (A = s(A, M.props), Ua(A, M), A.return = x, A) : (A = Zl(
        M.type,
        M.key,
        M.props,
        null,
        x.mode,
        U
      ), Ua(A, M), A.return = x, A);
    }
    function D(x, A, M, U) {
      return A === null || A.tag !== 4 || A.stateNode.containerInfo !== M.containerInfo || A.stateNode.implementation !== M.implementation ? (A = no(M, x.mode, U), A.return = x, A) : (A = s(A, M.children || []), A.return = x, A);
    }
    function V(x, A, M, U, I) {
      return A === null || A.tag !== 7 ? (A = ni(
        M,
        x.mode,
        U,
        I
      ), A.return = x, A) : (A = s(A, M), A.return = x, A);
    }
    function B(x, A, M) {
      if (typeof A == "string" && A !== "" || typeof A == "number" || typeof A == "bigint")
        return A = eo(
          "" + A,
          x.mode,
          M
        ), A.return = x, A;
      if (typeof A == "object" && A !== null) {
        switch (A.$$typeof) {
          case _:
            return M = Zl(
              A.type,
              A.key,
              A.props,
              null,
              x.mode,
              M
            ), Ua(M, A), M.return = x, M;
          case z:
            return A = no(
              A,
              x.mode,
              M
            ), A.return = x, A;
          case K:
            return A = ui(A), B(x, A, M);
        }
        if (wt(A) || vt(A))
          return A = ni(
            A,
            x.mode,
            M,
            null
          ), A.return = x, A;
        if (typeof A.then == "function")
          return B(x, Pl(A), M);
        if (A.$$typeof === H)
          return B(
            x,
            Jl(x, A),
            M
          );
        $l(x, A);
      }
      return null;
    }
    function C(x, A, M, U) {
      var I = A !== null ? A.key : null;
      if (typeof M == "string" && M !== "" || typeof M == "number" || typeof M == "bigint")
        return I !== null ? null : p(x, A, "" + M, U);
      if (typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case _:
            return M.key === I ? T(x, A, M, U) : null;
          case z:
            return M.key === I ? D(x, A, M, U) : null;
          case K:
            return M = ui(M), C(x, A, M, U);
        }
        if (wt(M) || vt(M))
          return I !== null ? null : V(x, A, M, U, null);
        if (typeof M.then == "function")
          return C(
            x,
            A,
            Pl(M),
            U
          );
        if (M.$$typeof === H)
          return C(
            x,
            A,
            Jl(x, M),
            U
          );
        $l(x, M);
      }
      return null;
    }
    function R(x, A, M, U, I) {
      if (typeof U == "string" && U !== "" || typeof U == "number" || typeof U == "bigint")
        return x = x.get(M) || null, p(A, x, "" + U, I);
      if (typeof U == "object" && U !== null) {
        switch (U.$$typeof) {
          case _:
            return x = x.get(
              U.key === null ? M : U.key
            ) || null, T(A, x, U, I);
          case z:
            return x = x.get(
              U.key === null ? M : U.key
            ) || null, D(A, x, U, I);
          case K:
            return U = ui(U), R(
              x,
              A,
              M,
              U,
              I
            );
        }
        if (wt(U) || vt(U))
          return x = x.get(M) || null, V(A, x, U, I, null);
        if (typeof U.then == "function")
          return R(
            x,
            A,
            M,
            Pl(U),
            I
          );
        if (U.$$typeof === H)
          return R(
            x,
            A,
            M,
            Jl(A, U),
            I
          );
        $l(A, U);
      }
      return null;
    }
    function k(x, A, M, U) {
      for (var I = null, St = null, P = A, ot = A = 0, mt = null; P !== null && ot < M.length; ot++) {
        P.index > ot ? (mt = P, P = null) : mt = P.sibling;
        var Tt = C(
          x,
          P,
          M[ot],
          U
        );
        if (Tt === null) {
          P === null && (P = mt);
          break;
        }
        t && P && Tt.alternate === null && e(x, P), A = r(Tt, A, ot), St === null ? I = Tt : St.sibling = Tt, St = Tt, P = mt;
      }
      if (ot === M.length)
        return n(x, P), gt && ln(x, ot), I;
      if (P === null) {
        for (; ot < M.length; ot++)
          P = B(x, M[ot], U), P !== null && (A = r(
            P,
            A,
            ot
          ), St === null ? I = P : St.sibling = P, St = P);
        return gt && ln(x, ot), I;
      }
      for (P = a(P); ot < M.length; ot++)
        mt = R(
          P,
          x,
          ot,
          M[ot],
          U
        ), mt !== null && (t && mt.alternate !== null && P.delete(
          mt.key === null ? ot : mt.key
        ), A = r(
          mt,
          A,
          ot
        ), St === null ? I = mt : St.sibling = mt, St = mt);
      return t && P.forEach(function(Zn) {
        return e(x, Zn);
      }), gt && ln(x, ot), I;
    }
    function et(x, A, M, U) {
      if (M == null) throw Error(o(151));
      for (var I = null, St = null, P = A, ot = A = 0, mt = null, Tt = M.next(); P !== null && !Tt.done; ot++, Tt = M.next()) {
        P.index > ot ? (mt = P, P = null) : mt = P.sibling;
        var Zn = C(x, P, Tt.value, U);
        if (Zn === null) {
          P === null && (P = mt);
          break;
        }
        t && P && Zn.alternate === null && e(x, P), A = r(Zn, A, ot), St === null ? I = Zn : St.sibling = Zn, St = Zn, P = mt;
      }
      if (Tt.done)
        return n(x, P), gt && ln(x, ot), I;
      if (P === null) {
        for (; !Tt.done; ot++, Tt = M.next())
          Tt = B(x, Tt.value, U), Tt !== null && (A = r(Tt, A, ot), St === null ? I = Tt : St.sibling = Tt, St = Tt);
        return gt && ln(x, ot), I;
      }
      for (P = a(P); !Tt.done; ot++, Tt = M.next())
        Tt = R(P, x, ot, Tt.value, U), Tt !== null && (t && Tt.alternate !== null && P.delete(Tt.key === null ? ot : Tt.key), A = r(Tt, A, ot), St === null ? I = Tt : St.sibling = Tt, St = Tt);
      return t && P.forEach(function(G1) {
        return e(x, G1);
      }), gt && ln(x, ot), I;
    }
    function Ct(x, A, M, U) {
      if (typeof M == "object" && M !== null && M.type === j && M.key === null && (M = M.props.children), typeof M == "object" && M !== null) {
        switch (M.$$typeof) {
          case _:
            t: {
              for (var I = M.key; A !== null; ) {
                if (A.key === I) {
                  if (I = M.type, I === j) {
                    if (A.tag === 7) {
                      n(
                        x,
                        A.sibling
                      ), U = s(
                        A,
                        M.props.children
                      ), U.return = x, x = U;
                      break t;
                    }
                  } else if (A.elementType === I || typeof I == "object" && I !== null && I.$$typeof === K && ui(I) === A.type) {
                    n(
                      x,
                      A.sibling
                    ), U = s(A, M.props), Ua(U, M), U.return = x, x = U;
                    break t;
                  }
                  n(x, A);
                  break;
                } else e(x, A);
                A = A.sibling;
              }
              M.type === j ? (U = ni(
                M.props.children,
                x.mode,
                U,
                M.key
              ), U.return = x, x = U) : (U = Zl(
                M.type,
                M.key,
                M.props,
                null,
                x.mode,
                U
              ), Ua(U, M), U.return = x, x = U);
            }
            return f(x);
          case z:
            t: {
              for (I = M.key; A !== null; ) {
                if (A.key === I)
                  if (A.tag === 4 && A.stateNode.containerInfo === M.containerInfo && A.stateNode.implementation === M.implementation) {
                    n(
                      x,
                      A.sibling
                    ), U = s(A, M.children || []), U.return = x, x = U;
                    break t;
                  } else {
                    n(x, A);
                    break;
                  }
                else e(x, A);
                A = A.sibling;
              }
              U = no(M, x.mode, U), U.return = x, x = U;
            }
            return f(x);
          case K:
            return M = ui(M), Ct(
              x,
              A,
              M,
              U
            );
        }
        if (wt(M))
          return k(
            x,
            A,
            M,
            U
          );
        if (vt(M)) {
          if (I = vt(M), typeof I != "function") throw Error(o(150));
          return M = I.call(M), et(
            x,
            A,
            M,
            U
          );
        }
        if (typeof M.then == "function")
          return Ct(
            x,
            A,
            Pl(M),
            U
          );
        if (M.$$typeof === H)
          return Ct(
            x,
            A,
            Jl(x, M),
            U
          );
        $l(x, M);
      }
      return typeof M == "string" && M !== "" || typeof M == "number" || typeof M == "bigint" ? (M = "" + M, A !== null && A.tag === 6 ? (n(x, A.sibling), U = s(A, M), U.return = x, x = U) : (n(x, A), U = eo(M, x.mode, U), U.return = x, x = U), f(x)) : n(x, A);
    }
    return function(x, A, M, U) {
      try {
        _a = 0;
        var I = Ct(
          x,
          A,
          M,
          U
        );
        return qi = null, I;
      } catch (P) {
        if (P === Yi || P === Fl) throw P;
        var St = be(29, P, null, x.mode);
        return St.lanes = U, St.return = x, St;
      }
    };
  }
  var ri = Eh(!0), xh = Eh(!1), Cn = !1;
  function yo(t) {
    t.updateQueue = {
      baseState: t.memoizedState,
      firstBaseUpdate: null,
      lastBaseUpdate: null,
      shared: { pending: null, lanes: 0, hiddenCallbacks: null },
      callbacks: null
    };
  }
  function po(t, e) {
    t = t.updateQueue, e.updateQueue === t && (e.updateQueue = {
      baseState: t.baseState,
      firstBaseUpdate: t.firstBaseUpdate,
      lastBaseUpdate: t.lastBaseUpdate,
      shared: t.shared,
      callbacks: null
    });
  }
  function zn(t) {
    return { lane: t, tag: 0, payload: null, callback: null, next: null };
  }
  function Rn(t, e, n) {
    var a = t.updateQueue;
    if (a === null) return null;
    if (a = a.shared, (bt & 2) !== 0) {
      var s = a.pending;
      return s === null ? e.next = e : (e.next = s.next, s.next = e), a.pending = e, e = Xl(t), uh(t, null, n), e;
    }
    return Gl(t, a, e, n), Xl(t);
  }
  function Ba(t, e, n) {
    if (e = e.updateQueue, e !== null && (e = e.shared, (n & 4194048) !== 0)) {
      var a = e.lanes;
      a &= t.pendingLanes, n |= a, e.lanes = n, yf(t, n);
    }
  }
  function go(t, e) {
    var n = t.updateQueue, a = t.alternate;
    if (a !== null && (a = a.updateQueue, n === a)) {
      var s = null, r = null;
      if (n = n.firstBaseUpdate, n !== null) {
        do {
          var f = {
            lane: n.lane,
            tag: n.tag,
            payload: n.payload,
            callback: null,
            next: null
          };
          r === null ? s = r = f : r = r.next = f, n = n.next;
        } while (n !== null);
        r === null ? s = r = e : r = r.next = e;
      } else s = r = e;
      n = {
        baseState: a.baseState,
        firstBaseUpdate: s,
        lastBaseUpdate: r,
        shared: a.shared,
        callbacks: a.callbacks
      }, t.updateQueue = n;
      return;
    }
    t = n.lastBaseUpdate, t === null ? n.firstBaseUpdate = e : t.next = e, n.lastBaseUpdate = e;
  }
  var vo = !1;
  function Na() {
    if (vo) {
      var t = Hi;
      if (t !== null) throw t;
    }
  }
  function ja(t, e, n, a) {
    vo = !1;
    var s = t.updateQueue;
    Cn = !1;
    var r = s.firstBaseUpdate, f = s.lastBaseUpdate, p = s.shared.pending;
    if (p !== null) {
      s.shared.pending = null;
      var T = p, D = T.next;
      T.next = null, f === null ? r = D : f.next = D, f = T;
      var V = t.alternate;
      V !== null && (V = V.updateQueue, p = V.lastBaseUpdate, p !== f && (p === null ? V.firstBaseUpdate = D : p.next = D, V.lastBaseUpdate = T));
    }
    if (r !== null) {
      var B = s.baseState;
      f = 0, V = D = T = null, p = r;
      do {
        var C = p.lane & -536870913, R = C !== p.lane;
        if (R ? (dt & C) === C : (a & C) === C) {
          C !== 0 && C === Li && (vo = !0), V !== null && (V = V.next = {
            lane: 0,
            tag: p.tag,
            payload: p.payload,
            callback: null,
            next: null
          });
          t: {
            var k = t, et = p;
            C = e;
            var Ct = n;
            switch (et.tag) {
              case 1:
                if (k = et.payload, typeof k == "function") {
                  B = k.call(Ct, B, C);
                  break t;
                }
                B = k;
                break t;
              case 3:
                k.flags = k.flags & -65537 | 128;
              case 0:
                if (k = et.payload, C = typeof k == "function" ? k.call(Ct, B, C) : k, C == null) break t;
                B = S({}, B, C);
                break t;
              case 2:
                Cn = !0;
            }
          }
          C = p.callback, C !== null && (t.flags |= 64, R && (t.flags |= 8192), R = s.callbacks, R === null ? s.callbacks = [C] : R.push(C));
        } else
          R = {
            lane: C,
            tag: p.tag,
            payload: p.payload,
            callback: p.callback,
            next: null
          }, V === null ? (D = V = R, T = B) : V = V.next = R, f |= C;
        if (p = p.next, p === null) {
          if (p = s.shared.pending, p === null)
            break;
          R = p, p = R.next, R.next = null, s.lastBaseUpdate = R, s.shared.pending = null;
        }
      } while (!0);
      V === null && (T = B), s.baseState = T, s.firstBaseUpdate = D, s.lastBaseUpdate = V, r === null && (s.shared.lanes = 0), Bn |= f, t.lanes = f, t.memoizedState = B;
    }
  }
  function Mh(t, e) {
    if (typeof t != "function")
      throw Error(o(191, t));
    t.call(e);
  }
  function Dh(t, e) {
    var n = t.callbacks;
    if (n !== null)
      for (t.callbacks = null, t = 0; t < n.length; t++)
        Mh(n[t], e);
  }
  var Gi = E(null), Il = E(0);
  function Ch(t, e) {
    t = pn, Z(Il, t), Z(Gi, e), pn = t | e.baseLanes;
  }
  function So() {
    Z(Il, pn), Z(Gi, Gi.current);
  }
  function To() {
    pn = Il.current, N(Gi), N(Il);
  }
  var Ae = E(null), Ne = null;
  function On(t) {
    var e = t.alternate;
    Z(Ht, Ht.current & 1), Z(Ae, t), Ne === null && (e === null || Gi.current !== null || e.memoizedState !== null) && (Ne = t);
  }
  function bo(t) {
    Z(Ht, Ht.current), Z(Ae, t), Ne === null && (Ne = t);
  }
  function zh(t) {
    t.tag === 22 ? (Z(Ht, Ht.current), Z(Ae, t), Ne === null && (Ne = t)) : Vn();
  }
  function Vn() {
    Z(Ht, Ht.current), Z(Ae, Ae.current);
  }
  function Ee(t) {
    N(Ae), Ne === t && (Ne = null), N(Ht);
  }
  var Ht = E(0);
  function ts(t) {
    for (var e = t; e !== null; ) {
      if (e.tag === 13) {
        var n = e.memoizedState;
        if (n !== null && (n = n.dehydrated, n === null || Cr(n) || zr(n)))
          return e;
      } else if (e.tag === 19 && (e.memoizedProps.revealOrder === "forwards" || e.memoizedProps.revealOrder === "backwards" || e.memoizedProps.revealOrder === "unstable_legacy-backwards" || e.memoizedProps.revealOrder === "together")) {
        if ((e.flags & 128) !== 0) return e;
      } else if (e.child !== null) {
        e.child.return = e, e = e.child;
        continue;
      }
      if (e === t) break;
      for (; e.sibling === null; ) {
        if (e.return === null || e.return === t) return null;
        e = e.return;
      }
      e.sibling.return = e.return, e = e.sibling;
    }
    return null;
  }
  var on = 0, st = null, Mt = null, Xt = null, es = !1, Xi = !1, ci = !1, ns = 0, wa = 0, Zi = null, _v = 0;
  function Bt() {
    throw Error(o(321));
  }
  function Ao(t, e) {
    if (e === null) return !1;
    for (var n = 0; n < e.length && n < t.length; n++)
      if (!Te(t[n], e[n])) return !1;
    return !0;
  }
  function Eo(t, e, n, a, s, r) {
    return on = r, st = e, e.memoizedState = null, e.updateQueue = null, e.lanes = 0, O.H = t === null || t.memoizedState === null ? fd : Lo, ci = !1, r = n(a, s), ci = !1, Xi && (r = Oh(
      e,
      n,
      a,
      s
    )), Rh(t), r;
  }
  function Rh(t) {
    O.H = Ya;
    var e = Mt !== null && Mt.next !== null;
    if (on = 0, Xt = Mt = st = null, es = !1, wa = 0, Zi = null, e) throw Error(o(300));
    t === null || Zt || (t = t.dependencies, t !== null && Kl(t) && (Zt = !0));
  }
  function Oh(t, e, n, a) {
    st = t;
    var s = 0;
    do {
      if (Xi && (Zi = null), wa = 0, Xi = !1, 25 <= s) throw Error(o(301));
      if (s += 1, Xt = Mt = null, t.updateQueue != null) {
        var r = t.updateQueue;
        r.lastEffect = null, r.events = null, r.stores = null, r.memoCache != null && (r.memoCache.index = 0);
      }
      O.H = hd, r = e(n, a);
    } while (Xi);
    return r;
  }
  function Uv() {
    var t = O.H, e = t.useState()[0];
    return e = typeof e.then == "function" ? La(e) : e, t = t.useState()[0], (Mt !== null ? Mt.memoizedState : null) !== t && (st.flags |= 1024), e;
  }
  function xo() {
    var t = ns !== 0;
    return ns = 0, t;
  }
  function Mo(t, e, n) {
    e.updateQueue = t.updateQueue, e.flags &= -2053, t.lanes &= ~n;
  }
  function Do(t) {
    if (es) {
      for (t = t.memoizedState; t !== null; ) {
        var e = t.queue;
        e !== null && (e.pending = null), t = t.next;
      }
      es = !1;
    }
    on = 0, Xt = Mt = st = null, Xi = !1, wa = ns = 0, Zi = null;
  }
  function ue() {
    var t = {
      memoizedState: null,
      baseState: null,
      baseQueue: null,
      queue: null,
      next: null
    };
    return Xt === null ? st.memoizedState = Xt = t : Xt = Xt.next = t, Xt;
  }
  function Yt() {
    if (Mt === null) {
      var t = st.alternate;
      t = t !== null ? t.memoizedState : null;
    } else t = Mt.next;
    var e = Xt === null ? st.memoizedState : Xt.next;
    if (e !== null)
      Xt = e, Mt = t;
    else {
      if (t === null)
        throw st.alternate === null ? Error(o(467)) : Error(o(310));
      Mt = t, t = {
        memoizedState: Mt.memoizedState,
        baseState: Mt.baseState,
        baseQueue: Mt.baseQueue,
        queue: Mt.queue,
        next: null
      }, Xt === null ? st.memoizedState = Xt = t : Xt = Xt.next = t;
    }
    return Xt;
  }
  function is() {
    return { lastEffect: null, events: null, stores: null, memoCache: null };
  }
  function La(t) {
    var e = wa;
    return wa += 1, Zi === null && (Zi = []), t = Th(Zi, t, e), e = st, (Xt === null ? e.memoizedState : Xt.next) === null && (e = e.alternate, O.H = e === null || e.memoizedState === null ? fd : Lo), t;
  }
  function as(t) {
    if (t !== null && typeof t == "object") {
      if (typeof t.then == "function") return La(t);
      if (t.$$typeof === H) return te(t);
    }
    throw Error(o(438, String(t)));
  }
  function Co(t) {
    var e = null, n = st.updateQueue;
    if (n !== null && (e = n.memoCache), e == null) {
      var a = st.alternate;
      a !== null && (a = a.updateQueue, a !== null && (a = a.memoCache, a != null && (e = {
        data: a.data.map(function(s) {
          return s.slice();
        }),
        index: 0
      })));
    }
    if (e == null && (e = { data: [], index: 0 }), n === null && (n = is(), st.updateQueue = n), n.memoCache = e, n = e.data[e.index], n === void 0)
      for (n = e.data[e.index] = Array(t), a = 0; a < t; a++)
        n[a] = $;
    return e.index++, n;
  }
  function rn(t, e) {
    return typeof e == "function" ? e(t) : e;
  }
  function ls(t) {
    var e = Yt();
    return zo(e, Mt, t);
  }
  function zo(t, e, n) {
    var a = t.queue;
    if (a === null) throw Error(o(311));
    a.lastRenderedReducer = n;
    var s = t.baseQueue, r = a.pending;
    if (r !== null) {
      if (s !== null) {
        var f = s.next;
        s.next = r.next, r.next = f;
      }
      e.baseQueue = s = r, a.pending = null;
    }
    if (r = t.baseState, s === null) t.memoizedState = r;
    else {
      e = s.next;
      var p = f = null, T = null, D = e, V = !1;
      do {
        var B = D.lane & -536870913;
        if (B !== D.lane ? (dt & B) === B : (on & B) === B) {
          var C = D.revertLane;
          if (C === 0)
            T !== null && (T = T.next = {
              lane: 0,
              revertLane: 0,
              gesture: null,
              action: D.action,
              hasEagerState: D.hasEagerState,
              eagerState: D.eagerState,
              next: null
            }), B === Li && (V = !0);
          else if ((on & C) === C) {
            D = D.next, C === Li && (V = !0);
            continue;
          } else
            B = {
              lane: 0,
              revertLane: D.revertLane,
              gesture: null,
              action: D.action,
              hasEagerState: D.hasEagerState,
              eagerState: D.eagerState,
              next: null
            }, T === null ? (p = T = B, f = r) : T = T.next = B, st.lanes |= C, Bn |= C;
          B = D.action, ci && n(r, B), r = D.hasEagerState ? D.eagerState : n(r, B);
        } else
          C = {
            lane: B,
            revertLane: D.revertLane,
            gesture: D.gesture,
            action: D.action,
            hasEagerState: D.hasEagerState,
            eagerState: D.eagerState,
            next: null
          }, T === null ? (p = T = C, f = r) : T = T.next = C, st.lanes |= B, Bn |= B;
        D = D.next;
      } while (D !== null && D !== e);
      if (T === null ? f = r : T.next = p, !Te(r, t.memoizedState) && (Zt = !0, V && (n = Hi, n !== null)))
        throw n;
      t.memoizedState = r, t.baseState = f, t.baseQueue = T, a.lastRenderedState = r;
    }
    return s === null && (a.lanes = 0), [t.memoizedState, a.dispatch];
  }
  function Ro(t) {
    var e = Yt(), n = e.queue;
    if (n === null) throw Error(o(311));
    n.lastRenderedReducer = t;
    var a = n.dispatch, s = n.pending, r = e.memoizedState;
    if (s !== null) {
      n.pending = null;
      var f = s = s.next;
      do
        r = t(r, f.action), f = f.next;
      while (f !== s);
      Te(r, e.memoizedState) || (Zt = !0), e.memoizedState = r, e.baseQueue === null && (e.baseState = r), n.lastRenderedState = r;
    }
    return [r, a];
  }
  function Vh(t, e, n) {
    var a = st, s = Yt(), r = gt;
    if (r) {
      if (n === void 0) throw Error(o(407));
      n = n();
    } else n = e();
    var f = !Te(
      (Mt || s).memoizedState,
      n
    );
    if (f && (s.memoizedState = n, Zt = !0), s = s.queue, _o(Bh.bind(null, a, s, t), [
      t
    ]), s.getSnapshot !== e || f || Xt !== null && Xt.memoizedState.tag & 1) {
      if (a.flags |= 2048, Qi(
        9,
        { destroy: void 0 },
        Uh.bind(
          null,
          a,
          s,
          n,
          e
        ),
        null
      ), zt === null) throw Error(o(349));
      r || (on & 127) !== 0 || _h(a, e, n);
    }
    return n;
  }
  function _h(t, e, n) {
    t.flags |= 16384, t = { getSnapshot: e, value: n }, e = st.updateQueue, e === null ? (e = is(), st.updateQueue = e, e.stores = [t]) : (n = e.stores, n === null ? e.stores = [t] : n.push(t));
  }
  function Uh(t, e, n, a) {
    e.value = n, e.getSnapshot = a, Nh(e) && jh(t);
  }
  function Bh(t, e, n) {
    return n(function() {
      Nh(e) && jh(t);
    });
  }
  function Nh(t) {
    var e = t.getSnapshot;
    t = t.value;
    try {
      var n = e();
      return !Te(t, n);
    } catch {
      return !0;
    }
  }
  function jh(t) {
    var e = ei(t, 2);
    e !== null && pe(e, t, 2);
  }
  function Oo(t) {
    var e = ue();
    if (typeof t == "function") {
      var n = t;
      if (t = n(), ci) {
        Tn(!0);
        try {
          n();
        } finally {
          Tn(!1);
        }
      }
    }
    return e.memoizedState = e.baseState = t, e.queue = {
      pending: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: rn,
      lastRenderedState: t
    }, e;
  }
  function wh(t, e, n, a) {
    return t.baseState = n, zo(
      t,
      Mt,
      typeof a == "function" ? a : rn
    );
  }
  function Bv(t, e, n, a, s) {
    if (os(t)) throw Error(o(485));
    if (t = e.action, t !== null) {
      var r = {
        payload: s,
        action: t,
        next: null,
        isTransition: !0,
        status: "pending",
        value: null,
        reason: null,
        listeners: [],
        then: function(f) {
          r.listeners.push(f);
        }
      };
      O.T !== null ? n(!0) : r.isTransition = !1, a(r), n = e.pending, n === null ? (r.next = e.pending = r, Lh(e, r)) : (r.next = n.next, e.pending = n.next = r);
    }
  }
  function Lh(t, e) {
    var n = e.action, a = e.payload, s = t.state;
    if (e.isTransition) {
      var r = O.T, f = {};
      O.T = f;
      try {
        var p = n(s, a), T = O.S;
        T !== null && T(f, p), Hh(t, e, p);
      } catch (D) {
        Vo(t, e, D);
      } finally {
        r !== null && f.types !== null && (r.types = f.types), O.T = r;
      }
    } else
      try {
        r = n(s, a), Hh(t, e, r);
      } catch (D) {
        Vo(t, e, D);
      }
  }
  function Hh(t, e, n) {
    n !== null && typeof n == "object" && typeof n.then == "function" ? n.then(
      function(a) {
        Yh(t, e, a);
      },
      function(a) {
        return Vo(t, e, a);
      }
    ) : Yh(t, e, n);
  }
  function Yh(t, e, n) {
    e.status = "fulfilled", e.value = n, qh(e), t.state = n, e = t.pending, e !== null && (n = e.next, n === e ? t.pending = null : (n = n.next, e.next = n, Lh(t, n)));
  }
  function Vo(t, e, n) {
    var a = t.pending;
    if (t.pending = null, a !== null) {
      a = a.next;
      do
        e.status = "rejected", e.reason = n, qh(e), e = e.next;
      while (e !== a);
    }
    t.action = null;
  }
  function qh(t) {
    t = t.listeners;
    for (var e = 0; e < t.length; e++) (0, t[e])();
  }
  function Gh(t, e) {
    return e;
  }
  function Xh(t, e) {
    if (gt) {
      var n = zt.formState;
      if (n !== null) {
        t: {
          var a = st;
          if (gt) {
            if (Vt) {
              e: {
                for (var s = Vt, r = Be; s.nodeType !== 8; ) {
                  if (!r) {
                    s = null;
                    break e;
                  }
                  if (s = je(
                    s.nextSibling
                  ), s === null) {
                    s = null;
                    break e;
                  }
                }
                r = s.data, s = r === "F!" || r === "F" ? s : null;
              }
              if (s) {
                Vt = je(
                  s.nextSibling
                ), a = s.data === "F!";
                break t;
              }
            }
            Mn(a);
          }
          a = !1;
        }
        a && (e = n[0]);
      }
    }
    return n = ue(), n.memoizedState = n.baseState = e, a = {
      pending: null,
      lanes: 0,
      dispatch: null,
      lastRenderedReducer: Gh,
      lastRenderedState: e
    }, n.queue = a, n = od.bind(
      null,
      st,
      a
    ), a.dispatch = n, a = Oo(!1), r = wo.bind(
      null,
      st,
      !1,
      a.queue
    ), a = ue(), s = {
      state: e,
      dispatch: null,
      action: t,
      pending: null
    }, a.queue = s, n = Bv.bind(
      null,
      st,
      s,
      r,
      n
    ), s.dispatch = n, a.memoizedState = t, [e, n, !1];
  }
  function Zh(t) {
    var e = Yt();
    return Qh(e, Mt, t);
  }
  function Qh(t, e, n) {
    if (e = zo(
      t,
      e,
      Gh
    )[0], t = ls(rn)[0], typeof e == "object" && e !== null && typeof e.then == "function")
      try {
        var a = La(e);
      } catch (f) {
        throw f === Yi ? Fl : f;
      }
    else a = e;
    e = Yt();
    var s = e.queue, r = s.dispatch;
    return n !== e.memoizedState && (st.flags |= 2048, Qi(
      9,
      { destroy: void 0 },
      Nv.bind(null, s, n),
      null
    )), [a, r, t];
  }
  function Nv(t, e) {
    t.action = e;
  }
  function Kh(t) {
    var e = Yt(), n = Mt;
    if (n !== null)
      return Qh(e, n, t);
    Yt(), e = e.memoizedState, n = Yt();
    var a = n.queue.dispatch;
    return n.memoizedState = t, [e, a, !1];
  }
  function Qi(t, e, n, a) {
    return t = { tag: t, create: n, deps: a, inst: e, next: null }, e = st.updateQueue, e === null && (e = is(), st.updateQueue = e), n = e.lastEffect, n === null ? e.lastEffect = t.next = t : (a = n.next, n.next = t, t.next = a, e.lastEffect = t), t;
  }
  function Jh() {
    return Yt().memoizedState;
  }
  function ss(t, e, n, a) {
    var s = ue();
    st.flags |= t, s.memoizedState = Qi(
      1 | e,
      { destroy: void 0 },
      n,
      a === void 0 ? null : a
    );
  }
  function us(t, e, n, a) {
    var s = Yt();
    a = a === void 0 ? null : a;
    var r = s.memoizedState.inst;
    Mt !== null && a !== null && Ao(a, Mt.memoizedState.deps) ? s.memoizedState = Qi(e, r, n, a) : (st.flags |= t, s.memoizedState = Qi(
      1 | e,
      r,
      n,
      a
    ));
  }
  function kh(t, e) {
    ss(8390656, 8, t, e);
  }
  function _o(t, e) {
    us(2048, 8, t, e);
  }
  function jv(t) {
    st.flags |= 4;
    var e = st.updateQueue;
    if (e === null)
      e = is(), st.updateQueue = e, e.events = [t];
    else {
      var n = e.events;
      n === null ? e.events = [t] : n.push(t);
    }
  }
  function Fh(t) {
    var e = Yt().memoizedState;
    return jv({ ref: e, nextImpl: t }), function() {
      if ((bt & 2) !== 0) throw Error(o(440));
      return e.impl.apply(void 0, arguments);
    };
  }
  function Wh(t, e) {
    return us(4, 2, t, e);
  }
  function Ph(t, e) {
    return us(4, 4, t, e);
  }
  function $h(t, e) {
    if (typeof e == "function") {
      t = t();
      var n = e(t);
      return function() {
        typeof n == "function" ? n() : e(null);
      };
    }
    if (e != null)
      return t = t(), e.current = t, function() {
        e.current = null;
      };
  }
  function Ih(t, e, n) {
    n = n != null ? n.concat([t]) : null, us(4, 4, $h.bind(null, e, t), n);
  }
  function Uo() {
  }
  function td(t, e) {
    var n = Yt();
    e = e === void 0 ? null : e;
    var a = n.memoizedState;
    return e !== null && Ao(e, a[1]) ? a[0] : (n.memoizedState = [t, e], t);
  }
  function ed(t, e) {
    var n = Yt();
    e = e === void 0 ? null : e;
    var a = n.memoizedState;
    if (e !== null && Ao(e, a[1]))
      return a[0];
    if (a = t(), ci) {
      Tn(!0);
      try {
        t();
      } finally {
        Tn(!1);
      }
    }
    return n.memoizedState = [a, e], a;
  }
  function Bo(t, e, n) {
    return n === void 0 || (on & 1073741824) !== 0 && (dt & 261930) === 0 ? t.memoizedState = e : (t.memoizedState = n, t = nm(), st.lanes |= t, Bn |= t, n);
  }
  function nd(t, e, n, a) {
    return Te(n, e) ? n : Gi.current !== null ? (t = Bo(t, n, a), Te(t, e) || (Zt = !0), t) : (on & 42) === 0 || (on & 1073741824) !== 0 && (dt & 261930) === 0 ? (Zt = !0, t.memoizedState = n) : (t = nm(), st.lanes |= t, Bn |= t, e);
  }
  function id(t, e, n, a, s) {
    var r = X.p;
    X.p = r !== 0 && 8 > r ? r : 8;
    var f = O.T, p = {};
    O.T = p, wo(t, !1, e, n);
    try {
      var T = s(), D = O.S;
      if (D !== null && D(p, T), T !== null && typeof T == "object" && typeof T.then == "function") {
        var V = Vv(
          T,
          a
        );
        Ha(
          t,
          e,
          V,
          De(t)
        );
      } else
        Ha(
          t,
          e,
          a,
          De(t)
        );
    } catch (B) {
      Ha(
        t,
        e,
        { then: function() {
        }, status: "rejected", reason: B },
        De()
      );
    } finally {
      X.p = r, f !== null && p.types !== null && (f.types = p.types), O.T = f;
    }
  }
  function wv() {
  }
  function No(t, e, n, a) {
    if (t.tag !== 5) throw Error(o(476));
    var s = ad(t).queue;
    id(
      t,
      s,
      e,
      J,
      n === null ? wv : function() {
        return ld(t), n(a);
      }
    );
  }
  function ad(t) {
    var e = t.memoizedState;
    if (e !== null) return e;
    e = {
      memoizedState: J,
      baseState: J,
      baseQueue: null,
      queue: {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: rn,
        lastRenderedState: J
      },
      next: null
    };
    var n = {};
    return e.next = {
      memoizedState: n,
      baseState: n,
      baseQueue: null,
      queue: {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: rn,
        lastRenderedState: n
      },
      next: null
    }, t.memoizedState = e, t = t.alternate, t !== null && (t.memoizedState = e), e;
  }
  function ld(t) {
    var e = ad(t);
    e.next === null && (e = t.alternate.memoizedState), Ha(
      t,
      e.next.queue,
      {},
      De()
    );
  }
  function jo() {
    return te(nl);
  }
  function sd() {
    return Yt().memoizedState;
  }
  function ud() {
    return Yt().memoizedState;
  }
  function Lv(t) {
    for (var e = t.return; e !== null; ) {
      switch (e.tag) {
        case 24:
        case 3:
          var n = De();
          t = zn(n);
          var a = Rn(e, t, n);
          a !== null && (pe(a, e, n), Ba(a, e, n)), e = { cache: co() }, t.payload = e;
          return;
      }
      e = e.return;
    }
  }
  function Hv(t, e, n) {
    var a = De();
    n = {
      lane: a,
      revertLane: 0,
      gesture: null,
      action: n,
      hasEagerState: !1,
      eagerState: null,
      next: null
    }, os(t) ? rd(e, n) : (n = Iu(t, e, n, a), n !== null && (pe(n, t, a), cd(n, e, a)));
  }
  function od(t, e, n) {
    var a = De();
    Ha(t, e, n, a);
  }
  function Ha(t, e, n, a) {
    var s = {
      lane: a,
      revertLane: 0,
      gesture: null,
      action: n,
      hasEagerState: !1,
      eagerState: null,
      next: null
    };
    if (os(t)) rd(e, s);
    else {
      var r = t.alternate;
      if (t.lanes === 0 && (r === null || r.lanes === 0) && (r = e.lastRenderedReducer, r !== null))
        try {
          var f = e.lastRenderedState, p = r(f, n);
          if (s.hasEagerState = !0, s.eagerState = p, Te(p, f))
            return Gl(t, e, s, 0), zt === null && ql(), !1;
        } catch {
        }
      if (n = Iu(t, e, s, a), n !== null)
        return pe(n, t, a), cd(n, e, a), !0;
    }
    return !1;
  }
  function wo(t, e, n, a) {
    if (a = {
      lane: 2,
      revertLane: yr(),
      gesture: null,
      action: a,
      hasEagerState: !1,
      eagerState: null,
      next: null
    }, os(t)) {
      if (e) throw Error(o(479));
    } else
      e = Iu(
        t,
        n,
        a,
        2
      ), e !== null && pe(e, t, 2);
  }
  function os(t) {
    var e = t.alternate;
    return t === st || e !== null && e === st;
  }
  function rd(t, e) {
    Xi = es = !0;
    var n = t.pending;
    n === null ? e.next = e : (e.next = n.next, n.next = e), t.pending = e;
  }
  function cd(t, e, n) {
    if ((n & 4194048) !== 0) {
      var a = e.lanes;
      a &= t.pendingLanes, n |= a, e.lanes = n, yf(t, n);
    }
  }
  var Ya = {
    readContext: te,
    use: as,
    useCallback: Bt,
    useContext: Bt,
    useEffect: Bt,
    useImperativeHandle: Bt,
    useLayoutEffect: Bt,
    useInsertionEffect: Bt,
    useMemo: Bt,
    useReducer: Bt,
    useRef: Bt,
    useState: Bt,
    useDebugValue: Bt,
    useDeferredValue: Bt,
    useTransition: Bt,
    useSyncExternalStore: Bt,
    useId: Bt,
    useHostTransitionStatus: Bt,
    useFormState: Bt,
    useActionState: Bt,
    useOptimistic: Bt,
    useMemoCache: Bt,
    useCacheRefresh: Bt
  };
  Ya.useEffectEvent = Bt;
  var fd = {
    readContext: te,
    use: as,
    useCallback: function(t, e) {
      return ue().memoizedState = [
        t,
        e === void 0 ? null : e
      ], t;
    },
    useContext: te,
    useEffect: kh,
    useImperativeHandle: function(t, e, n) {
      n = n != null ? n.concat([t]) : null, ss(
        4194308,
        4,
        $h.bind(null, e, t),
        n
      );
    },
    useLayoutEffect: function(t, e) {
      return ss(4194308, 4, t, e);
    },
    useInsertionEffect: function(t, e) {
      ss(4, 2, t, e);
    },
    useMemo: function(t, e) {
      var n = ue();
      e = e === void 0 ? null : e;
      var a = t();
      if (ci) {
        Tn(!0);
        try {
          t();
        } finally {
          Tn(!1);
        }
      }
      return n.memoizedState = [a, e], a;
    },
    useReducer: function(t, e, n) {
      var a = ue();
      if (n !== void 0) {
        var s = n(e);
        if (ci) {
          Tn(!0);
          try {
            n(e);
          } finally {
            Tn(!1);
          }
        }
      } else s = e;
      return a.memoizedState = a.baseState = s, t = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: t,
        lastRenderedState: s
      }, a.queue = t, t = t.dispatch = Hv.bind(
        null,
        st,
        t
      ), [a.memoizedState, t];
    },
    useRef: function(t) {
      var e = ue();
      return t = { current: t }, e.memoizedState = t;
    },
    useState: function(t) {
      t = Oo(t);
      var e = t.queue, n = od.bind(null, st, e);
      return e.dispatch = n, [t.memoizedState, n];
    },
    useDebugValue: Uo,
    useDeferredValue: function(t, e) {
      var n = ue();
      return Bo(n, t, e);
    },
    useTransition: function() {
      var t = Oo(!1);
      return t = id.bind(
        null,
        st,
        t.queue,
        !0,
        !1
      ), ue().memoizedState = t, [!1, t];
    },
    useSyncExternalStore: function(t, e, n) {
      var a = st, s = ue();
      if (gt) {
        if (n === void 0)
          throw Error(o(407));
        n = n();
      } else {
        if (n = e(), zt === null)
          throw Error(o(349));
        (dt & 127) !== 0 || _h(a, e, n);
      }
      s.memoizedState = n;
      var r = { value: n, getSnapshot: e };
      return s.queue = r, kh(Bh.bind(null, a, r, t), [
        t
      ]), a.flags |= 2048, Qi(
        9,
        { destroy: void 0 },
        Uh.bind(
          null,
          a,
          r,
          n,
          e
        ),
        null
      ), n;
    },
    useId: function() {
      var t = ue(), e = zt.identifierPrefix;
      if (gt) {
        var n = Je, a = Ke;
        n = (a & ~(1 << 32 - Se(a) - 1)).toString(32) + n, e = "_" + e + "R_" + n, n = ns++, 0 < n && (e += "H" + n.toString(32)), e += "_";
      } else
        n = _v++, e = "_" + e + "r_" + n.toString(32) + "_";
      return t.memoizedState = e;
    },
    useHostTransitionStatus: jo,
    useFormState: Xh,
    useActionState: Xh,
    useOptimistic: function(t) {
      var e = ue();
      e.memoizedState = e.baseState = t;
      var n = {
        pending: null,
        lanes: 0,
        dispatch: null,
        lastRenderedReducer: null,
        lastRenderedState: null
      };
      return e.queue = n, e = wo.bind(
        null,
        st,
        !0,
        n
      ), n.dispatch = e, [t, e];
    },
    useMemoCache: Co,
    useCacheRefresh: function() {
      return ue().memoizedState = Lv.bind(
        null,
        st
      );
    },
    useEffectEvent: function(t) {
      var e = ue(), n = { impl: t };
      return e.memoizedState = n, function() {
        if ((bt & 2) !== 0)
          throw Error(o(440));
        return n.impl.apply(void 0, arguments);
      };
    }
  }, Lo = {
    readContext: te,
    use: as,
    useCallback: td,
    useContext: te,
    useEffect: _o,
    useImperativeHandle: Ih,
    useInsertionEffect: Wh,
    useLayoutEffect: Ph,
    useMemo: ed,
    useReducer: ls,
    useRef: Jh,
    useState: function() {
      return ls(rn);
    },
    useDebugValue: Uo,
    useDeferredValue: function(t, e) {
      var n = Yt();
      return nd(
        n,
        Mt.memoizedState,
        t,
        e
      );
    },
    useTransition: function() {
      var t = ls(rn)[0], e = Yt().memoizedState;
      return [
        typeof t == "boolean" ? t : La(t),
        e
      ];
    },
    useSyncExternalStore: Vh,
    useId: sd,
    useHostTransitionStatus: jo,
    useFormState: Zh,
    useActionState: Zh,
    useOptimistic: function(t, e) {
      var n = Yt();
      return wh(n, Mt, t, e);
    },
    useMemoCache: Co,
    useCacheRefresh: ud
  };
  Lo.useEffectEvent = Fh;
  var hd = {
    readContext: te,
    use: as,
    useCallback: td,
    useContext: te,
    useEffect: _o,
    useImperativeHandle: Ih,
    useInsertionEffect: Wh,
    useLayoutEffect: Ph,
    useMemo: ed,
    useReducer: Ro,
    useRef: Jh,
    useState: function() {
      return Ro(rn);
    },
    useDebugValue: Uo,
    useDeferredValue: function(t, e) {
      var n = Yt();
      return Mt === null ? Bo(n, t, e) : nd(
        n,
        Mt.memoizedState,
        t,
        e
      );
    },
    useTransition: function() {
      var t = Ro(rn)[0], e = Yt().memoizedState;
      return [
        typeof t == "boolean" ? t : La(t),
        e
      ];
    },
    useSyncExternalStore: Vh,
    useId: sd,
    useHostTransitionStatus: jo,
    useFormState: Kh,
    useActionState: Kh,
    useOptimistic: function(t, e) {
      var n = Yt();
      return Mt !== null ? wh(n, Mt, t, e) : (n.baseState = t, [t, n.queue.dispatch]);
    },
    useMemoCache: Co,
    useCacheRefresh: ud
  };
  hd.useEffectEvent = Fh;
  function Ho(t, e, n, a) {
    e = t.memoizedState, n = n(a, e), n = n == null ? e : S({}, e, n), t.memoizedState = n, t.lanes === 0 && (t.updateQueue.baseState = n);
  }
  var Yo = {
    enqueueSetState: function(t, e, n) {
      t = t._reactInternals;
      var a = De(), s = zn(a);
      s.payload = e, n != null && (s.callback = n), e = Rn(t, s, a), e !== null && (pe(e, t, a), Ba(e, t, a));
    },
    enqueueReplaceState: function(t, e, n) {
      t = t._reactInternals;
      var a = De(), s = zn(a);
      s.tag = 1, s.payload = e, n != null && (s.callback = n), e = Rn(t, s, a), e !== null && (pe(e, t, a), Ba(e, t, a));
    },
    enqueueForceUpdate: function(t, e) {
      t = t._reactInternals;
      var n = De(), a = zn(n);
      a.tag = 2, e != null && (a.callback = e), e = Rn(t, a, n), e !== null && (pe(e, t, n), Ba(e, t, n));
    }
  };
  function dd(t, e, n, a, s, r, f) {
    return t = t.stateNode, typeof t.shouldComponentUpdate == "function" ? t.shouldComponentUpdate(a, r, f) : e.prototype && e.prototype.isPureReactComponent ? !Da(n, a) || !Da(s, r) : !0;
  }
  function md(t, e, n, a) {
    t = e.state, typeof e.componentWillReceiveProps == "function" && e.componentWillReceiveProps(n, a), typeof e.UNSAFE_componentWillReceiveProps == "function" && e.UNSAFE_componentWillReceiveProps(n, a), e.state !== t && Yo.enqueueReplaceState(e, e.state, null);
  }
  function fi(t, e) {
    var n = e;
    if ("ref" in e) {
      n = {};
      for (var a in e)
        a !== "ref" && (n[a] = e[a]);
    }
    if (t = t.defaultProps) {
      n === e && (n = S({}, n));
      for (var s in t)
        n[s] === void 0 && (n[s] = t[s]);
    }
    return n;
  }
  function yd(t) {
    Yl(t);
  }
  function pd(t) {
    console.error(t);
  }
  function gd(t) {
    Yl(t);
  }
  function rs(t, e) {
    try {
      var n = t.onUncaughtError;
      n(e.value, { componentStack: e.stack });
    } catch (a) {
      setTimeout(function() {
        throw a;
      });
    }
  }
  function vd(t, e, n) {
    try {
      var a = t.onCaughtError;
      a(n.value, {
        componentStack: n.stack,
        errorBoundary: e.tag === 1 ? e.stateNode : null
      });
    } catch (s) {
      setTimeout(function() {
        throw s;
      });
    }
  }
  function qo(t, e, n) {
    return n = zn(n), n.tag = 3, n.payload = { element: null }, n.callback = function() {
      rs(t, e);
    }, n;
  }
  function Sd(t) {
    return t = zn(t), t.tag = 3, t;
  }
  function Td(t, e, n, a) {
    var s = n.type.getDerivedStateFromError;
    if (typeof s == "function") {
      var r = a.value;
      t.payload = function() {
        return s(r);
      }, t.callback = function() {
        vd(e, n, a);
      };
    }
    var f = n.stateNode;
    f !== null && typeof f.componentDidCatch == "function" && (t.callback = function() {
      vd(e, n, a), typeof s != "function" && (Nn === null ? Nn = /* @__PURE__ */ new Set([this]) : Nn.add(this));
      var p = a.stack;
      this.componentDidCatch(a.value, {
        componentStack: p !== null ? p : ""
      });
    });
  }
  function Yv(t, e, n, a, s) {
    if (n.flags |= 32768, a !== null && typeof a == "object" && typeof a.then == "function") {
      if (e = n.alternate, e !== null && wi(
        e,
        n,
        s,
        !0
      ), n = Ae.current, n !== null) {
        switch (n.tag) {
          case 31:
          case 13:
            return Ne === null ? bs() : n.alternate === null && Nt === 0 && (Nt = 3), n.flags &= -257, n.flags |= 65536, n.lanes = s, a === Wl ? n.flags |= 16384 : (e = n.updateQueue, e === null ? n.updateQueue = /* @__PURE__ */ new Set([a]) : e.add(a), hr(t, a, s)), !1;
          case 22:
            return n.flags |= 65536, a === Wl ? n.flags |= 16384 : (e = n.updateQueue, e === null ? (e = {
              transitions: null,
              markerInstances: null,
              retryQueue: /* @__PURE__ */ new Set([a])
            }, n.updateQueue = e) : (n = e.retryQueue, n === null ? e.retryQueue = /* @__PURE__ */ new Set([a]) : n.add(a)), hr(t, a, s)), !1;
        }
        throw Error(o(435, n.tag));
      }
      return hr(t, a, s), bs(), !1;
    }
    if (gt)
      return e = Ae.current, e !== null ? ((e.flags & 65536) === 0 && (e.flags |= 256), e.flags |= 65536, e.lanes = s, a !== lo && (t = Error(o(422), { cause: a }), Ra(Ve(t, n)))) : (a !== lo && (e = Error(o(423), {
        cause: a
      }), Ra(
        Ve(e, n)
      )), t = t.current.alternate, t.flags |= 65536, s &= -s, t.lanes |= s, a = Ve(a, n), s = qo(
        t.stateNode,
        a,
        s
      ), go(t, s), Nt !== 4 && (Nt = 2)), !1;
    var r = Error(o(520), { cause: a });
    if (r = Ve(r, n), ka === null ? ka = [r] : ka.push(r), Nt !== 4 && (Nt = 2), e === null) return !0;
    a = Ve(a, n), n = e;
    do {
      switch (n.tag) {
        case 3:
          return n.flags |= 65536, t = s & -s, n.lanes |= t, t = qo(n.stateNode, a, t), go(n, t), !1;
        case 1:
          if (e = n.type, r = n.stateNode, (n.flags & 128) === 0 && (typeof e.getDerivedStateFromError == "function" || r !== null && typeof r.componentDidCatch == "function" && (Nn === null || !Nn.has(r))))
            return n.flags |= 65536, s &= -s, n.lanes |= s, s = Sd(s), Td(
              s,
              t,
              n,
              a
            ), go(n, s), !1;
      }
      n = n.return;
    } while (n !== null);
    return !1;
  }
  var Go = Error(o(461)), Zt = !1;
  function ee(t, e, n, a) {
    e.child = t === null ? xh(e, null, n, a) : ri(
      e,
      t.child,
      n,
      a
    );
  }
  function bd(t, e, n, a, s) {
    n = n.render;
    var r = e.ref;
    if ("ref" in a) {
      var f = {};
      for (var p in a)
        p !== "ref" && (f[p] = a[p]);
    } else f = a;
    return li(e), a = Eo(
      t,
      e,
      n,
      f,
      r,
      s
    ), p = xo(), t !== null && !Zt ? (Mo(t, e, s), cn(t, e, s)) : (gt && p && io(e), e.flags |= 1, ee(t, e, a, s), e.child);
  }
  function Ad(t, e, n, a, s) {
    if (t === null) {
      var r = n.type;
      return typeof r == "function" && !to(r) && r.defaultProps === void 0 && n.compare === null ? (e.tag = 15, e.type = r, Ed(
        t,
        e,
        r,
        a,
        s
      )) : (t = Zl(
        n.type,
        null,
        a,
        e,
        e.mode,
        s
      ), t.ref = e.ref, t.return = e, e.child = t);
    }
    if (r = t.child, !Wo(t, s)) {
      var f = r.memoizedProps;
      if (n = n.compare, n = n !== null ? n : Da, n(f, a) && t.ref === e.ref)
        return cn(t, e, s);
    }
    return e.flags |= 1, t = an(r, a), t.ref = e.ref, t.return = e, e.child = t;
  }
  function Ed(t, e, n, a, s) {
    if (t !== null) {
      var r = t.memoizedProps;
      if (Da(r, a) && t.ref === e.ref)
        if (Zt = !1, e.pendingProps = a = r, Wo(t, s))
          (t.flags & 131072) !== 0 && (Zt = !0);
        else
          return e.lanes = t.lanes, cn(t, e, s);
    }
    return Xo(
      t,
      e,
      n,
      a,
      s
    );
  }
  function xd(t, e, n, a) {
    var s = a.children, r = t !== null ? t.memoizedState : null;
    if (t === null && e.stateNode === null && (e.stateNode = {
      _visibility: 1,
      _pendingMarkers: null,
      _retryCache: null,
      _transitions: null
    }), a.mode === "hidden") {
      if ((e.flags & 128) !== 0) {
        if (r = r !== null ? r.baseLanes | n : n, t !== null) {
          for (a = e.child = t.child, s = 0; a !== null; )
            s = s | a.lanes | a.childLanes, a = a.sibling;
          a = s & ~r;
        } else a = 0, e.child = null;
        return Md(
          t,
          e,
          r,
          n,
          a
        );
      }
      if ((n & 536870912) !== 0)
        e.memoizedState = { baseLanes: 0, cachePool: null }, t !== null && kl(
          e,
          r !== null ? r.cachePool : null
        ), r !== null ? Ch(e, r) : So(), zh(e);
      else
        return a = e.lanes = 536870912, Md(
          t,
          e,
          r !== null ? r.baseLanes | n : n,
          n,
          a
        );
    } else
      r !== null ? (kl(e, r.cachePool), Ch(e, r), Vn(), e.memoizedState = null) : (t !== null && kl(e, null), So(), Vn());
    return ee(t, e, s, n), e.child;
  }
  function qa(t, e) {
    return t !== null && t.tag === 22 || e.stateNode !== null || (e.stateNode = {
      _visibility: 1,
      _pendingMarkers: null,
      _retryCache: null,
      _transitions: null
    }), e.sibling;
  }
  function Md(t, e, n, a, s) {
    var r = ho();
    return r = r === null ? null : { parent: Gt._currentValue, pool: r }, e.memoizedState = {
      baseLanes: n,
      cachePool: r
    }, t !== null && kl(e, null), So(), zh(e), t !== null && wi(t, e, a, !0), e.childLanes = s, null;
  }
  function cs(t, e) {
    return e = hs(
      { mode: e.mode, children: e.children },
      t.mode
    ), e.ref = t.ref, t.child = e, e.return = t, e;
  }
  function Dd(t, e, n) {
    return ri(e, t.child, null, n), t = cs(e, e.pendingProps), t.flags |= 2, Ee(e), e.memoizedState = null, t;
  }
  function qv(t, e, n) {
    var a = e.pendingProps, s = (e.flags & 128) !== 0;
    if (e.flags &= -129, t === null) {
      if (gt) {
        if (a.mode === "hidden")
          return t = cs(e, a), e.lanes = 536870912, qa(null, t);
        if (bo(e), (t = Vt) ? (t = Lm(
          t,
          Be
        ), t = t !== null && t.data === "&" ? t : null, t !== null && (e.memoizedState = {
          dehydrated: t,
          treeContext: En !== null ? { id: Ke, overflow: Je } : null,
          retryLane: 536870912,
          hydrationErrors: null
        }, n = rh(t), n.return = e, e.child = n, It = e, Vt = null)) : t = null, t === null) throw Mn(e);
        return e.lanes = 536870912, null;
      }
      return cs(e, a);
    }
    var r = t.memoizedState;
    if (r !== null) {
      var f = r.dehydrated;
      if (bo(e), s)
        if (e.flags & 256)
          e.flags &= -257, e = Dd(
            t,
            e,
            n
          );
        else if (e.memoizedState !== null)
          e.child = t.child, e.flags |= 128, e = null;
        else throw Error(o(558));
      else if (Zt || wi(t, e, n, !1), s = (n & t.childLanes) !== 0, Zt || s) {
        if (a = zt, a !== null && (f = pf(a, n), f !== 0 && f !== r.retryLane))
          throw r.retryLane = f, ei(t, f), pe(a, t, f), Go;
        bs(), e = Dd(
          t,
          e,
          n
        );
      } else
        t = r.treeContext, Vt = je(f.nextSibling), It = e, gt = !0, xn = null, Be = !1, t !== null && hh(e, t), e = cs(e, a), e.flags |= 4096;
      return e;
    }
    return t = an(t.child, {
      mode: a.mode,
      children: a.children
    }), t.ref = e.ref, e.child = t, t.return = e, t;
  }
  function fs(t, e) {
    var n = e.ref;
    if (n === null)
      t !== null && t.ref !== null && (e.flags |= 4194816);
    else {
      if (typeof n != "function" && typeof n != "object")
        throw Error(o(284));
      (t === null || t.ref !== n) && (e.flags |= 4194816);
    }
  }
  function Xo(t, e, n, a, s) {
    return li(e), n = Eo(
      t,
      e,
      n,
      a,
      void 0,
      s
    ), a = xo(), t !== null && !Zt ? (Mo(t, e, s), cn(t, e, s)) : (gt && a && io(e), e.flags |= 1, ee(t, e, n, s), e.child);
  }
  function Cd(t, e, n, a, s, r) {
    return li(e), e.updateQueue = null, n = Oh(
      e,
      a,
      n,
      s
    ), Rh(t), a = xo(), t !== null && !Zt ? (Mo(t, e, r), cn(t, e, r)) : (gt && a && io(e), e.flags |= 1, ee(t, e, n, r), e.child);
  }
  function zd(t, e, n, a, s) {
    if (li(e), e.stateNode === null) {
      var r = Ui, f = n.contextType;
      typeof f == "object" && f !== null && (r = te(f)), r = new n(a, r), e.memoizedState = r.state !== null && r.state !== void 0 ? r.state : null, r.updater = Yo, e.stateNode = r, r._reactInternals = e, r = e.stateNode, r.props = a, r.state = e.memoizedState, r.refs = {}, yo(e), f = n.contextType, r.context = typeof f == "object" && f !== null ? te(f) : Ui, r.state = e.memoizedState, f = n.getDerivedStateFromProps, typeof f == "function" && (Ho(
        e,
        n,
        f,
        a
      ), r.state = e.memoizedState), typeof n.getDerivedStateFromProps == "function" || typeof r.getSnapshotBeforeUpdate == "function" || typeof r.UNSAFE_componentWillMount != "function" && typeof r.componentWillMount != "function" || (f = r.state, typeof r.componentWillMount == "function" && r.componentWillMount(), typeof r.UNSAFE_componentWillMount == "function" && r.UNSAFE_componentWillMount(), f !== r.state && Yo.enqueueReplaceState(r, r.state, null), ja(e, a, r, s), Na(), r.state = e.memoizedState), typeof r.componentDidMount == "function" && (e.flags |= 4194308), a = !0;
    } else if (t === null) {
      r = e.stateNode;
      var p = e.memoizedProps, T = fi(n, p);
      r.props = T;
      var D = r.context, V = n.contextType;
      f = Ui, typeof V == "object" && V !== null && (f = te(V));
      var B = n.getDerivedStateFromProps;
      V = typeof B == "function" || typeof r.getSnapshotBeforeUpdate == "function", p = e.pendingProps !== p, V || typeof r.UNSAFE_componentWillReceiveProps != "function" && typeof r.componentWillReceiveProps != "function" || (p || D !== f) && md(
        e,
        r,
        a,
        f
      ), Cn = !1;
      var C = e.memoizedState;
      r.state = C, ja(e, a, r, s), Na(), D = e.memoizedState, p || C !== D || Cn ? (typeof B == "function" && (Ho(
        e,
        n,
        B,
        a
      ), D = e.memoizedState), (T = Cn || dd(
        e,
        n,
        T,
        a,
        C,
        D,
        f
      )) ? (V || typeof r.UNSAFE_componentWillMount != "function" && typeof r.componentWillMount != "function" || (typeof r.componentWillMount == "function" && r.componentWillMount(), typeof r.UNSAFE_componentWillMount == "function" && r.UNSAFE_componentWillMount()), typeof r.componentDidMount == "function" && (e.flags |= 4194308)) : (typeof r.componentDidMount == "function" && (e.flags |= 4194308), e.memoizedProps = a, e.memoizedState = D), r.props = a, r.state = D, r.context = f, a = T) : (typeof r.componentDidMount == "function" && (e.flags |= 4194308), a = !1);
    } else {
      r = e.stateNode, po(t, e), f = e.memoizedProps, V = fi(n, f), r.props = V, B = e.pendingProps, C = r.context, D = n.contextType, T = Ui, typeof D == "object" && D !== null && (T = te(D)), p = n.getDerivedStateFromProps, (D = typeof p == "function" || typeof r.getSnapshotBeforeUpdate == "function") || typeof r.UNSAFE_componentWillReceiveProps != "function" && typeof r.componentWillReceiveProps != "function" || (f !== B || C !== T) && md(
        e,
        r,
        a,
        T
      ), Cn = !1, C = e.memoizedState, r.state = C, ja(e, a, r, s), Na();
      var R = e.memoizedState;
      f !== B || C !== R || Cn || t !== null && t.dependencies !== null && Kl(t.dependencies) ? (typeof p == "function" && (Ho(
        e,
        n,
        p,
        a
      ), R = e.memoizedState), (V = Cn || dd(
        e,
        n,
        V,
        a,
        C,
        R,
        T
      ) || t !== null && t.dependencies !== null && Kl(t.dependencies)) ? (D || typeof r.UNSAFE_componentWillUpdate != "function" && typeof r.componentWillUpdate != "function" || (typeof r.componentWillUpdate == "function" && r.componentWillUpdate(a, R, T), typeof r.UNSAFE_componentWillUpdate == "function" && r.UNSAFE_componentWillUpdate(
        a,
        R,
        T
      )), typeof r.componentDidUpdate == "function" && (e.flags |= 4), typeof r.getSnapshotBeforeUpdate == "function" && (e.flags |= 1024)) : (typeof r.componentDidUpdate != "function" || f === t.memoizedProps && C === t.memoizedState || (e.flags |= 4), typeof r.getSnapshotBeforeUpdate != "function" || f === t.memoizedProps && C === t.memoizedState || (e.flags |= 1024), e.memoizedProps = a, e.memoizedState = R), r.props = a, r.state = R, r.context = T, a = V) : (typeof r.componentDidUpdate != "function" || f === t.memoizedProps && C === t.memoizedState || (e.flags |= 4), typeof r.getSnapshotBeforeUpdate != "function" || f === t.memoizedProps && C === t.memoizedState || (e.flags |= 1024), a = !1);
    }
    return r = a, fs(t, e), a = (e.flags & 128) !== 0, r || a ? (r = e.stateNode, n = a && typeof n.getDerivedStateFromError != "function" ? null : r.render(), e.flags |= 1, t !== null && a ? (e.child = ri(
      e,
      t.child,
      null,
      s
    ), e.child = ri(
      e,
      null,
      n,
      s
    )) : ee(t, e, n, s), e.memoizedState = r.state, t = e.child) : t = cn(
      t,
      e,
      s
    ), t;
  }
  function Rd(t, e, n, a) {
    return ii(), e.flags |= 256, ee(t, e, n, a), e.child;
  }
  var Zo = {
    dehydrated: null,
    treeContext: null,
    retryLane: 0,
    hydrationErrors: null
  };
  function Qo(t) {
    return { baseLanes: t, cachePool: vh() };
  }
  function Ko(t, e, n) {
    return t = t !== null ? t.childLanes & ~n : 0, e && (t |= Me), t;
  }
  function Od(t, e, n) {
    var a = e.pendingProps, s = !1, r = (e.flags & 128) !== 0, f;
    if ((f = r) || (f = t !== null && t.memoizedState === null ? !1 : (Ht.current & 2) !== 0), f && (s = !0, e.flags &= -129), f = (e.flags & 32) !== 0, e.flags &= -33, t === null) {
      if (gt) {
        if (s ? On(e) : Vn(), (t = Vt) ? (t = Lm(
          t,
          Be
        ), t = t !== null && t.data !== "&" ? t : null, t !== null && (e.memoizedState = {
          dehydrated: t,
          treeContext: En !== null ? { id: Ke, overflow: Je } : null,
          retryLane: 536870912,
          hydrationErrors: null
        }, n = rh(t), n.return = e, e.child = n, It = e, Vt = null)) : t = null, t === null) throw Mn(e);
        return zr(t) ? e.lanes = 32 : e.lanes = 536870912, null;
      }
      var p = a.children;
      return a = a.fallback, s ? (Vn(), s = e.mode, p = hs(
        { mode: "hidden", children: p },
        s
      ), a = ni(
        a,
        s,
        n,
        null
      ), p.return = e, a.return = e, p.sibling = a, e.child = p, a = e.child, a.memoizedState = Qo(n), a.childLanes = Ko(
        t,
        f,
        n
      ), e.memoizedState = Zo, qa(null, a)) : (On(e), Jo(e, p));
    }
    var T = t.memoizedState;
    if (T !== null && (p = T.dehydrated, p !== null)) {
      if (r)
        e.flags & 256 ? (On(e), e.flags &= -257, e = ko(
          t,
          e,
          n
        )) : e.memoizedState !== null ? (Vn(), e.child = t.child, e.flags |= 128, e = null) : (Vn(), p = a.fallback, s = e.mode, a = hs(
          { mode: "visible", children: a.children },
          s
        ), p = ni(
          p,
          s,
          n,
          null
        ), p.flags |= 2, a.return = e, p.return = e, a.sibling = p, e.child = a, ri(
          e,
          t.child,
          null,
          n
        ), a = e.child, a.memoizedState = Qo(n), a.childLanes = Ko(
          t,
          f,
          n
        ), e.memoizedState = Zo, e = qa(null, a));
      else if (On(e), zr(p)) {
        if (f = p.nextSibling && p.nextSibling.dataset, f) var D = f.dgst;
        f = D, a = Error(o(419)), a.stack = "", a.digest = f, Ra({ value: a, source: null, stack: null }), e = ko(
          t,
          e,
          n
        );
      } else if (Zt || wi(t, e, n, !1), f = (n & t.childLanes) !== 0, Zt || f) {
        if (f = zt, f !== null && (a = pf(f, n), a !== 0 && a !== T.retryLane))
          throw T.retryLane = a, ei(t, a), pe(f, t, a), Go;
        Cr(p) || bs(), e = ko(
          t,
          e,
          n
        );
      } else
        Cr(p) ? (e.flags |= 192, e.child = t.child, e = null) : (t = T.treeContext, Vt = je(
          p.nextSibling
        ), It = e, gt = !0, xn = null, Be = !1, t !== null && hh(e, t), e = Jo(
          e,
          a.children
        ), e.flags |= 4096);
      return e;
    }
    return s ? (Vn(), p = a.fallback, s = e.mode, T = t.child, D = T.sibling, a = an(T, {
      mode: "hidden",
      children: a.children
    }), a.subtreeFlags = T.subtreeFlags & 65011712, D !== null ? p = an(
      D,
      p
    ) : (p = ni(
      p,
      s,
      n,
      null
    ), p.flags |= 2), p.return = e, a.return = e, a.sibling = p, e.child = a, qa(null, a), a = e.child, p = t.child.memoizedState, p === null ? p = Qo(n) : (s = p.cachePool, s !== null ? (T = Gt._currentValue, s = s.parent !== T ? { parent: T, pool: T } : s) : s = vh(), p = {
      baseLanes: p.baseLanes | n,
      cachePool: s
    }), a.memoizedState = p, a.childLanes = Ko(
      t,
      f,
      n
    ), e.memoizedState = Zo, qa(t.child, a)) : (On(e), n = t.child, t = n.sibling, n = an(n, {
      mode: "visible",
      children: a.children
    }), n.return = e, n.sibling = null, t !== null && (f = e.deletions, f === null ? (e.deletions = [t], e.flags |= 16) : f.push(t)), e.child = n, e.memoizedState = null, n);
  }
  function Jo(t, e) {
    return e = hs(
      { mode: "visible", children: e },
      t.mode
    ), e.return = t, t.child = e;
  }
  function hs(t, e) {
    return t = be(22, t, null, e), t.lanes = 0, t;
  }
  function ko(t, e, n) {
    return ri(e, t.child, null, n), t = Jo(
      e,
      e.pendingProps.children
    ), t.flags |= 2, e.memoizedState = null, t;
  }
  function Vd(t, e, n) {
    t.lanes |= e;
    var a = t.alternate;
    a !== null && (a.lanes |= e), oo(t.return, e, n);
  }
  function Fo(t, e, n, a, s, r) {
    var f = t.memoizedState;
    f === null ? t.memoizedState = {
      isBackwards: e,
      rendering: null,
      renderingStartTime: 0,
      last: a,
      tail: n,
      tailMode: s,
      treeForkCount: r
    } : (f.isBackwards = e, f.rendering = null, f.renderingStartTime = 0, f.last = a, f.tail = n, f.tailMode = s, f.treeForkCount = r);
  }
  function _d(t, e, n) {
    var a = e.pendingProps, s = a.revealOrder, r = a.tail;
    a = a.children;
    var f = Ht.current, p = (f & 2) !== 0;
    if (p ? (f = f & 1 | 2, e.flags |= 128) : f &= 1, Z(Ht, f), ee(t, e, a, n), a = gt ? za : 0, !p && t !== null && (t.flags & 128) !== 0)
      t: for (t = e.child; t !== null; ) {
        if (t.tag === 13)
          t.memoizedState !== null && Vd(t, n, e);
        else if (t.tag === 19)
          Vd(t, n, e);
        else if (t.child !== null) {
          t.child.return = t, t = t.child;
          continue;
        }
        if (t === e) break t;
        for (; t.sibling === null; ) {
          if (t.return === null || t.return === e)
            break t;
          t = t.return;
        }
        t.sibling.return = t.return, t = t.sibling;
      }
    switch (s) {
      case "forwards":
        for (n = e.child, s = null; n !== null; )
          t = n.alternate, t !== null && ts(t) === null && (s = n), n = n.sibling;
        n = s, n === null ? (s = e.child, e.child = null) : (s = n.sibling, n.sibling = null), Fo(
          e,
          !1,
          s,
          n,
          r,
          a
        );
        break;
      case "backwards":
      case "unstable_legacy-backwards":
        for (n = null, s = e.child, e.child = null; s !== null; ) {
          if (t = s.alternate, t !== null && ts(t) === null) {
            e.child = s;
            break;
          }
          t = s.sibling, s.sibling = n, n = s, s = t;
        }
        Fo(
          e,
          !0,
          n,
          null,
          r,
          a
        );
        break;
      case "together":
        Fo(
          e,
          !1,
          null,
          null,
          void 0,
          a
        );
        break;
      default:
        e.memoizedState = null;
    }
    return e.child;
  }
  function cn(t, e, n) {
    if (t !== null && (e.dependencies = t.dependencies), Bn |= e.lanes, (n & e.childLanes) === 0)
      if (t !== null) {
        if (wi(
          t,
          e,
          n,
          !1
        ), (n & e.childLanes) === 0)
          return null;
      } else return null;
    if (t !== null && e.child !== t.child)
      throw Error(o(153));
    if (e.child !== null) {
      for (t = e.child, n = an(t, t.pendingProps), e.child = n, n.return = e; t.sibling !== null; )
        t = t.sibling, n = n.sibling = an(t, t.pendingProps), n.return = e;
      n.sibling = null;
    }
    return e.child;
  }
  function Wo(t, e) {
    return (t.lanes & e) !== 0 ? !0 : (t = t.dependencies, !!(t !== null && Kl(t)));
  }
  function Gv(t, e, n) {
    switch (e.tag) {
      case 3:
        se(e, e.stateNode.containerInfo), Dn(e, Gt, t.memoizedState.cache), ii();
        break;
      case 27:
      case 5:
        da(e);
        break;
      case 4:
        se(e, e.stateNode.containerInfo);
        break;
      case 10:
        Dn(
          e,
          e.type,
          e.memoizedProps.value
        );
        break;
      case 31:
        if (e.memoizedState !== null)
          return e.flags |= 128, bo(e), null;
        break;
      case 13:
        var a = e.memoizedState;
        if (a !== null)
          return a.dehydrated !== null ? (On(e), e.flags |= 128, null) : (n & e.child.childLanes) !== 0 ? Od(t, e, n) : (On(e), t = cn(
            t,
            e,
            n
          ), t !== null ? t.sibling : null);
        On(e);
        break;
      case 19:
        var s = (t.flags & 128) !== 0;
        if (a = (n & e.childLanes) !== 0, a || (wi(
          t,
          e,
          n,
          !1
        ), a = (n & e.childLanes) !== 0), s) {
          if (a)
            return _d(
              t,
              e,
              n
            );
          e.flags |= 128;
        }
        if (s = e.memoizedState, s !== null && (s.rendering = null, s.tail = null, s.lastEffect = null), Z(Ht, Ht.current), a) break;
        return null;
      case 22:
        return e.lanes = 0, xd(
          t,
          e,
          n,
          e.pendingProps
        );
      case 24:
        Dn(e, Gt, t.memoizedState.cache);
    }
    return cn(t, e, n);
  }
  function Ud(t, e, n) {
    if (t !== null)
      if (t.memoizedProps !== e.pendingProps)
        Zt = !0;
      else {
        if (!Wo(t, n) && (e.flags & 128) === 0)
          return Zt = !1, Gv(
            t,
            e,
            n
          );
        Zt = (t.flags & 131072) !== 0;
      }
    else
      Zt = !1, gt && (e.flags & 1048576) !== 0 && fh(e, za, e.index);
    switch (e.lanes = 0, e.tag) {
      case 16:
        t: {
          var a = e.pendingProps;
          if (t = ui(e.elementType), e.type = t, typeof t == "function")
            to(t) ? (a = fi(t, a), e.tag = 1, e = zd(
              null,
              e,
              t,
              a,
              n
            )) : (e.tag = 0, e = Xo(
              null,
              e,
              t,
              a,
              n
            ));
          else {
            if (t != null) {
              var s = t.$$typeof;
              if (s === Y) {
                e.tag = 11, e = bd(
                  null,
                  e,
                  t,
                  a,
                  n
                );
                break t;
              } else if (s === Q) {
                e.tag = 14, e = Ad(
                  null,
                  e,
                  t,
                  a,
                  n
                );
                break t;
              }
            }
            throw e = qt(t) || t, Error(o(306, e, ""));
          }
        }
        return e;
      case 0:
        return Xo(
          t,
          e,
          e.type,
          e.pendingProps,
          n
        );
      case 1:
        return a = e.type, s = fi(
          a,
          e.pendingProps
        ), zd(
          t,
          e,
          a,
          s,
          n
        );
      case 3:
        t: {
          if (se(
            e,
            e.stateNode.containerInfo
          ), t === null) throw Error(o(387));
          a = e.pendingProps;
          var r = e.memoizedState;
          s = r.element, po(t, e), ja(e, a, null, n);
          var f = e.memoizedState;
          if (a = f.cache, Dn(e, Gt, a), a !== r.cache && ro(
            e,
            [Gt],
            n,
            !0
          ), Na(), a = f.element, r.isDehydrated)
            if (r = {
              element: a,
              isDehydrated: !1,
              cache: f.cache
            }, e.updateQueue.baseState = r, e.memoizedState = r, e.flags & 256) {
              e = Rd(
                t,
                e,
                a,
                n
              );
              break t;
            } else if (a !== s) {
              s = Ve(
                Error(o(424)),
                e
              ), Ra(s), e = Rd(
                t,
                e,
                a,
                n
              );
              break t;
            } else
              for (t = e.stateNode.containerInfo, t.nodeType === 9 ? t = t.body : t = t.nodeName === "HTML" ? t.ownerDocument.body : t, Vt = je(t.firstChild), It = e, gt = !0, xn = null, Be = !0, n = xh(
                e,
                null,
                a,
                n
              ), e.child = n; n; )
                n.flags = n.flags & -3 | 4096, n = n.sibling;
          else {
            if (ii(), a === s) {
              e = cn(
                t,
                e,
                n
              );
              break t;
            }
            ee(t, e, a, n);
          }
          e = e.child;
        }
        return e;
      case 26:
        return fs(t, e), t === null ? (n = Zm(
          e.type,
          null,
          e.pendingProps,
          null
        )) ? e.memoizedState = n : gt || (n = e.type, t = e.pendingProps, a = zs(
          ct.current
        ).createElement(n), a[$t] = e, a[ce] = t, ne(a, n, t), Ft(a), e.stateNode = a) : e.memoizedState = Zm(
          e.type,
          t.memoizedProps,
          e.pendingProps,
          t.memoizedState
        ), null;
      case 27:
        return da(e), t === null && gt && (a = e.stateNode = qm(
          e.type,
          e.pendingProps,
          ct.current
        ), It = e, Be = !0, s = Vt, Hn(e.type) ? (Rr = s, Vt = je(a.firstChild)) : Vt = s), ee(
          t,
          e,
          e.pendingProps.children,
          n
        ), fs(t, e), t === null && (e.flags |= 4194304), e.child;
      case 5:
        return t === null && gt && ((s = a = Vt) && (a = v1(
          a,
          e.type,
          e.pendingProps,
          Be
        ), a !== null ? (e.stateNode = a, It = e, Vt = je(a.firstChild), Be = !1, s = !0) : s = !1), s || Mn(e)), da(e), s = e.type, r = e.pendingProps, f = t !== null ? t.memoizedProps : null, a = r.children, xr(s, r) ? a = null : f !== null && xr(s, f) && (e.flags |= 32), e.memoizedState !== null && (s = Eo(
          t,
          e,
          Uv,
          null,
          null,
          n
        ), nl._currentValue = s), fs(t, e), ee(t, e, a, n), e.child;
      case 6:
        return t === null && gt && ((t = n = Vt) && (n = S1(
          n,
          e.pendingProps,
          Be
        ), n !== null ? (e.stateNode = n, It = e, Vt = null, t = !0) : t = !1), t || Mn(e)), null;
      case 13:
        return Od(t, e, n);
      case 4:
        return se(
          e,
          e.stateNode.containerInfo
        ), a = e.pendingProps, t === null ? e.child = ri(
          e,
          null,
          a,
          n
        ) : ee(t, e, a, n), e.child;
      case 11:
        return bd(
          t,
          e,
          e.type,
          e.pendingProps,
          n
        );
      case 7:
        return ee(
          t,
          e,
          e.pendingProps,
          n
        ), e.child;
      case 8:
        return ee(
          t,
          e,
          e.pendingProps.children,
          n
        ), e.child;
      case 12:
        return ee(
          t,
          e,
          e.pendingProps.children,
          n
        ), e.child;
      case 10:
        return a = e.pendingProps, Dn(e, e.type, a.value), ee(t, e, a.children, n), e.child;
      case 9:
        return s = e.type._context, a = e.pendingProps.children, li(e), s = te(s), a = a(s), e.flags |= 1, ee(t, e, a, n), e.child;
      case 14:
        return Ad(
          t,
          e,
          e.type,
          e.pendingProps,
          n
        );
      case 15:
        return Ed(
          t,
          e,
          e.type,
          e.pendingProps,
          n
        );
      case 19:
        return _d(t, e, n);
      case 31:
        return qv(t, e, n);
      case 22:
        return xd(
          t,
          e,
          n,
          e.pendingProps
        );
      case 24:
        return li(e), a = te(Gt), t === null ? (s = ho(), s === null && (s = zt, r = co(), s.pooledCache = r, r.refCount++, r !== null && (s.pooledCacheLanes |= n), s = r), e.memoizedState = { parent: a, cache: s }, yo(e), Dn(e, Gt, s)) : ((t.lanes & n) !== 0 && (po(t, e), ja(e, null, null, n), Na()), s = t.memoizedState, r = e.memoizedState, s.parent !== a ? (s = { parent: a, cache: a }, e.memoizedState = s, e.lanes === 0 && (e.memoizedState = e.updateQueue.baseState = s), Dn(e, Gt, a)) : (a = r.cache, Dn(e, Gt, a), a !== s.cache && ro(
          e,
          [Gt],
          n,
          !0
        ))), ee(
          t,
          e,
          e.pendingProps.children,
          n
        ), e.child;
      case 29:
        throw e.pendingProps;
    }
    throw Error(o(156, e.tag));
  }
  function fn(t) {
    t.flags |= 4;
  }
  function Po(t, e, n, a, s) {
    if ((e = (t.mode & 32) !== 0) && (e = !1), e) {
      if (t.flags |= 16777216, (s & 335544128) === s)
        if (t.stateNode.complete) t.flags |= 8192;
        else if (sm()) t.flags |= 8192;
        else
          throw oi = Wl, mo;
    } else t.flags &= -16777217;
  }
  function Bd(t, e) {
    if (e.type !== "stylesheet" || (e.state.loading & 4) !== 0)
      t.flags &= -16777217;
    else if (t.flags |= 16777216, !Fm(e))
      if (sm()) t.flags |= 8192;
      else
        throw oi = Wl, mo;
  }
  function ds(t, e) {
    e !== null && (t.flags |= 4), t.flags & 16384 && (e = t.tag !== 22 ? df() : 536870912, t.lanes |= e, Fi |= e);
  }
  function Ga(t, e) {
    if (!gt)
      switch (t.tailMode) {
        case "hidden":
          e = t.tail;
          for (var n = null; e !== null; )
            e.alternate !== null && (n = e), e = e.sibling;
          n === null ? t.tail = null : n.sibling = null;
          break;
        case "collapsed":
          n = t.tail;
          for (var a = null; n !== null; )
            n.alternate !== null && (a = n), n = n.sibling;
          a === null ? e || t.tail === null ? t.tail = null : t.tail.sibling = null : a.sibling = null;
      }
  }
  function _t(t) {
    var e = t.alternate !== null && t.alternate.child === t.child, n = 0, a = 0;
    if (e)
      for (var s = t.child; s !== null; )
        n |= s.lanes | s.childLanes, a |= s.subtreeFlags & 65011712, a |= s.flags & 65011712, s.return = t, s = s.sibling;
    else
      for (s = t.child; s !== null; )
        n |= s.lanes | s.childLanes, a |= s.subtreeFlags, a |= s.flags, s.return = t, s = s.sibling;
    return t.subtreeFlags |= a, t.childLanes = n, e;
  }
  function Xv(t, e, n) {
    var a = e.pendingProps;
    switch (ao(e), e.tag) {
      case 16:
      case 15:
      case 0:
      case 11:
      case 7:
      case 8:
      case 12:
      case 9:
      case 14:
        return _t(e), null;
      case 1:
        return _t(e), null;
      case 3:
        return n = e.stateNode, a = null, t !== null && (a = t.memoizedState.cache), e.memoizedState.cache !== a && (e.flags |= 2048), un(Gt), Lt(), n.pendingContext && (n.context = n.pendingContext, n.pendingContext = null), (t === null || t.child === null) && (ji(e) ? fn(e) : t === null || t.memoizedState.isDehydrated && (e.flags & 256) === 0 || (e.flags |= 1024, so())), _t(e), null;
      case 26:
        var s = e.type, r = e.memoizedState;
        return t === null ? (fn(e), r !== null ? (_t(e), Bd(e, r)) : (_t(e), Po(
          e,
          s,
          null,
          a,
          n
        ))) : r ? r !== t.memoizedState ? (fn(e), _t(e), Bd(e, r)) : (_t(e), e.flags &= -16777217) : (t = t.memoizedProps, t !== a && fn(e), _t(e), Po(
          e,
          s,
          t,
          a,
          n
        )), null;
      case 27:
        if (xl(e), n = ct.current, s = e.type, t !== null && e.stateNode != null)
          t.memoizedProps !== a && fn(e);
        else {
          if (!a) {
            if (e.stateNode === null)
              throw Error(o(166));
            return _t(e), null;
          }
          t = W.current, ji(e) ? dh(e) : (t = qm(s, a, n), e.stateNode = t, fn(e));
        }
        return _t(e), null;
      case 5:
        if (xl(e), s = e.type, t !== null && e.stateNode != null)
          t.memoizedProps !== a && fn(e);
        else {
          if (!a) {
            if (e.stateNode === null)
              throw Error(o(166));
            return _t(e), null;
          }
          if (r = W.current, ji(e))
            dh(e);
          else {
            var f = zs(
              ct.current
            );
            switch (r) {
              case 1:
                r = f.createElementNS(
                  "http://www.w3.org/2000/svg",
                  s
                );
                break;
              case 2:
                r = f.createElementNS(
                  "http://www.w3.org/1998/Math/MathML",
                  s
                );
                break;
              default:
                switch (s) {
                  case "svg":
                    r = f.createElementNS(
                      "http://www.w3.org/2000/svg",
                      s
                    );
                    break;
                  case "math":
                    r = f.createElementNS(
                      "http://www.w3.org/1998/Math/MathML",
                      s
                    );
                    break;
                  case "script":
                    r = f.createElement("div"), r.innerHTML = "<script><\/script>", r = r.removeChild(
                      r.firstChild
                    );
                    break;
                  case "select":
                    r = typeof a.is == "string" ? f.createElement("select", {
                      is: a.is
                    }) : f.createElement("select"), a.multiple ? r.multiple = !0 : a.size && (r.size = a.size);
                    break;
                  default:
                    r = typeof a.is == "string" ? f.createElement(s, { is: a.is }) : f.createElement(s);
                }
            }
            r[$t] = e, r[ce] = a;
            t: for (f = e.child; f !== null; ) {
              if (f.tag === 5 || f.tag === 6)
                r.appendChild(f.stateNode);
              else if (f.tag !== 4 && f.tag !== 27 && f.child !== null) {
                f.child.return = f, f = f.child;
                continue;
              }
              if (f === e) break t;
              for (; f.sibling === null; ) {
                if (f.return === null || f.return === e)
                  break t;
                f = f.return;
              }
              f.sibling.return = f.return, f = f.sibling;
            }
            e.stateNode = r;
            t: switch (ne(r, s, a), s) {
              case "button":
              case "input":
              case "select":
              case "textarea":
                a = !!a.autoFocus;
                break t;
              case "img":
                a = !0;
                break t;
              default:
                a = !1;
            }
            a && fn(e);
          }
        }
        return _t(e), Po(
          e,
          e.type,
          t === null ? null : t.memoizedProps,
          e.pendingProps,
          n
        ), null;
      case 6:
        if (t && e.stateNode != null)
          t.memoizedProps !== a && fn(e);
        else {
          if (typeof a != "string" && e.stateNode === null)
            throw Error(o(166));
          if (t = ct.current, ji(e)) {
            if (t = e.stateNode, n = e.memoizedProps, a = null, s = It, s !== null)
              switch (s.tag) {
                case 27:
                case 5:
                  a = s.memoizedProps;
              }
            t[$t] = e, t = !!(t.nodeValue === n || a !== null && a.suppressHydrationWarning === !0 || Om(t.nodeValue, n)), t || Mn(e, !0);
          } else
            t = zs(t).createTextNode(
              a
            ), t[$t] = e, e.stateNode = t;
        }
        return _t(e), null;
      case 31:
        if (n = e.memoizedState, t === null || t.memoizedState !== null) {
          if (a = ji(e), n !== null) {
            if (t === null) {
              if (!a) throw Error(o(318));
              if (t = e.memoizedState, t = t !== null ? t.dehydrated : null, !t) throw Error(o(557));
              t[$t] = e;
            } else
              ii(), (e.flags & 128) === 0 && (e.memoizedState = null), e.flags |= 4;
            _t(e), t = !1;
          } else
            n = so(), t !== null && t.memoizedState !== null && (t.memoizedState.hydrationErrors = n), t = !0;
          if (!t)
            return e.flags & 256 ? (Ee(e), e) : (Ee(e), null);
          if ((e.flags & 128) !== 0)
            throw Error(o(558));
        }
        return _t(e), null;
      case 13:
        if (a = e.memoizedState, t === null || t.memoizedState !== null && t.memoizedState.dehydrated !== null) {
          if (s = ji(e), a !== null && a.dehydrated !== null) {
            if (t === null) {
              if (!s) throw Error(o(318));
              if (s = e.memoizedState, s = s !== null ? s.dehydrated : null, !s) throw Error(o(317));
              s[$t] = e;
            } else
              ii(), (e.flags & 128) === 0 && (e.memoizedState = null), e.flags |= 4;
            _t(e), s = !1;
          } else
            s = so(), t !== null && t.memoizedState !== null && (t.memoizedState.hydrationErrors = s), s = !0;
          if (!s)
            return e.flags & 256 ? (Ee(e), e) : (Ee(e), null);
        }
        return Ee(e), (e.flags & 128) !== 0 ? (e.lanes = n, e) : (n = a !== null, t = t !== null && t.memoizedState !== null, n && (a = e.child, s = null, a.alternate !== null && a.alternate.memoizedState !== null && a.alternate.memoizedState.cachePool !== null && (s = a.alternate.memoizedState.cachePool.pool), r = null, a.memoizedState !== null && a.memoizedState.cachePool !== null && (r = a.memoizedState.cachePool.pool), r !== s && (a.flags |= 2048)), n !== t && n && (e.child.flags |= 8192), ds(e, e.updateQueue), _t(e), null);
      case 4:
        return Lt(), t === null && Sr(e.stateNode.containerInfo), _t(e), null;
      case 10:
        return un(e.type), _t(e), null;
      case 19:
        if (N(Ht), a = e.memoizedState, a === null) return _t(e), null;
        if (s = (e.flags & 128) !== 0, r = a.rendering, r === null)
          if (s) Ga(a, !1);
          else {
            if (Nt !== 0 || t !== null && (t.flags & 128) !== 0)
              for (t = e.child; t !== null; ) {
                if (r = ts(t), r !== null) {
                  for (e.flags |= 128, Ga(a, !1), t = r.updateQueue, e.updateQueue = t, ds(e, t), e.subtreeFlags = 0, t = n, n = e.child; n !== null; )
                    oh(n, t), n = n.sibling;
                  return Z(
                    Ht,
                    Ht.current & 1 | 2
                  ), gt && ln(e, a.treeForkCount), e.child;
                }
                t = t.sibling;
              }
            a.tail !== null && ge() > vs && (e.flags |= 128, s = !0, Ga(a, !1), e.lanes = 4194304);
          }
        else {
          if (!s)
            if (t = ts(r), t !== null) {
              if (e.flags |= 128, s = !0, t = t.updateQueue, e.updateQueue = t, ds(e, t), Ga(a, !0), a.tail === null && a.tailMode === "hidden" && !r.alternate && !gt)
                return _t(e), null;
            } else
              2 * ge() - a.renderingStartTime > vs && n !== 536870912 && (e.flags |= 128, s = !0, Ga(a, !1), e.lanes = 4194304);
          a.isBackwards ? (r.sibling = e.child, e.child = r) : (t = a.last, t !== null ? t.sibling = r : e.child = r, a.last = r);
        }
        return a.tail !== null ? (t = a.tail, a.rendering = t, a.tail = t.sibling, a.renderingStartTime = ge(), t.sibling = null, n = Ht.current, Z(
          Ht,
          s ? n & 1 | 2 : n & 1
        ), gt && ln(e, a.treeForkCount), t) : (_t(e), null);
      case 22:
      case 23:
        return Ee(e), To(), a = e.memoizedState !== null, t !== null ? t.memoizedState !== null !== a && (e.flags |= 8192) : a && (e.flags |= 8192), a ? (n & 536870912) !== 0 && (e.flags & 128) === 0 && (_t(e), e.subtreeFlags & 6 && (e.flags |= 8192)) : _t(e), n = e.updateQueue, n !== null && ds(e, n.retryQueue), n = null, t !== null && t.memoizedState !== null && t.memoizedState.cachePool !== null && (n = t.memoizedState.cachePool.pool), a = null, e.memoizedState !== null && e.memoizedState.cachePool !== null && (a = e.memoizedState.cachePool.pool), a !== n && (e.flags |= 2048), t !== null && N(si), null;
      case 24:
        return n = null, t !== null && (n = t.memoizedState.cache), e.memoizedState.cache !== n && (e.flags |= 2048), un(Gt), _t(e), null;
      case 25:
        return null;
      case 30:
        return null;
    }
    throw Error(o(156, e.tag));
  }
  function Zv(t, e) {
    switch (ao(e), e.tag) {
      case 1:
        return t = e.flags, t & 65536 ? (e.flags = t & -65537 | 128, e) : null;
      case 3:
        return un(Gt), Lt(), t = e.flags, (t & 65536) !== 0 && (t & 128) === 0 ? (e.flags = t & -65537 | 128, e) : null;
      case 26:
      case 27:
      case 5:
        return xl(e), null;
      case 31:
        if (e.memoizedState !== null) {
          if (Ee(e), e.alternate === null)
            throw Error(o(340));
          ii();
        }
        return t = e.flags, t & 65536 ? (e.flags = t & -65537 | 128, e) : null;
      case 13:
        if (Ee(e), t = e.memoizedState, t !== null && t.dehydrated !== null) {
          if (e.alternate === null)
            throw Error(o(340));
          ii();
        }
        return t = e.flags, t & 65536 ? (e.flags = t & -65537 | 128, e) : null;
      case 19:
        return N(Ht), null;
      case 4:
        return Lt(), null;
      case 10:
        return un(e.type), null;
      case 22:
      case 23:
        return Ee(e), To(), t !== null && N(si), t = e.flags, t & 65536 ? (e.flags = t & -65537 | 128, e) : null;
      case 24:
        return un(Gt), null;
      case 25:
        return null;
      default:
        return null;
    }
  }
  function Nd(t, e) {
    switch (ao(e), e.tag) {
      case 3:
        un(Gt), Lt();
        break;
      case 26:
      case 27:
      case 5:
        xl(e);
        break;
      case 4:
        Lt();
        break;
      case 31:
        e.memoizedState !== null && Ee(e);
        break;
      case 13:
        Ee(e);
        break;
      case 19:
        N(Ht);
        break;
      case 10:
        un(e.type);
        break;
      case 22:
      case 23:
        Ee(e), To(), t !== null && N(si);
        break;
      case 24:
        un(Gt);
    }
  }
  function Xa(t, e) {
    try {
      var n = e.updateQueue, a = n !== null ? n.lastEffect : null;
      if (a !== null) {
        var s = a.next;
        n = s;
        do {
          if ((n.tag & t) === t) {
            a = void 0;
            var r = n.create, f = n.inst;
            a = r(), f.destroy = a;
          }
          n = n.next;
        } while (n !== s);
      }
    } catch (p) {
      xt(e, e.return, p);
    }
  }
  function _n(t, e, n) {
    try {
      var a = e.updateQueue, s = a !== null ? a.lastEffect : null;
      if (s !== null) {
        var r = s.next;
        a = r;
        do {
          if ((a.tag & t) === t) {
            var f = a.inst, p = f.destroy;
            if (p !== void 0) {
              f.destroy = void 0, s = e;
              var T = n, D = p;
              try {
                D();
              } catch (V) {
                xt(
                  s,
                  T,
                  V
                );
              }
            }
          }
          a = a.next;
        } while (a !== r);
      }
    } catch (V) {
      xt(e, e.return, V);
    }
  }
  function jd(t) {
    var e = t.updateQueue;
    if (e !== null) {
      var n = t.stateNode;
      try {
        Dh(e, n);
      } catch (a) {
        xt(t, t.return, a);
      }
    }
  }
  function wd(t, e, n) {
    n.props = fi(
      t.type,
      t.memoizedProps
    ), n.state = t.memoizedState;
    try {
      n.componentWillUnmount();
    } catch (a) {
      xt(t, e, a);
    }
  }
  function Za(t, e) {
    try {
      var n = t.ref;
      if (n !== null) {
        switch (t.tag) {
          case 26:
          case 27:
          case 5:
            var a = t.stateNode;
            break;
          case 30:
            a = t.stateNode;
            break;
          default:
            a = t.stateNode;
        }
        typeof n == "function" ? t.refCleanup = n(a) : n.current = a;
      }
    } catch (s) {
      xt(t, e, s);
    }
  }
  function ke(t, e) {
    var n = t.ref, a = t.refCleanup;
    if (n !== null)
      if (typeof a == "function")
        try {
          a();
        } catch (s) {
          xt(t, e, s);
        } finally {
          t.refCleanup = null, t = t.alternate, t != null && (t.refCleanup = null);
        }
      else if (typeof n == "function")
        try {
          n(null);
        } catch (s) {
          xt(t, e, s);
        }
      else n.current = null;
  }
  function Ld(t) {
    var e = t.type, n = t.memoizedProps, a = t.stateNode;
    try {
      t: switch (e) {
        case "button":
        case "input":
        case "select":
        case "textarea":
          n.autoFocus && a.focus();
          break t;
        case "img":
          n.src ? a.src = n.src : n.srcSet && (a.srcset = n.srcSet);
      }
    } catch (s) {
      xt(t, t.return, s);
    }
  }
  function $o(t, e, n) {
    try {
      var a = t.stateNode;
      h1(a, t.type, n, e), a[ce] = e;
    } catch (s) {
      xt(t, t.return, s);
    }
  }
  function Hd(t) {
    return t.tag === 5 || t.tag === 3 || t.tag === 26 || t.tag === 27 && Hn(t.type) || t.tag === 4;
  }
  function Io(t) {
    t: for (; ; ) {
      for (; t.sibling === null; ) {
        if (t.return === null || Hd(t.return)) return null;
        t = t.return;
      }
      for (t.sibling.return = t.return, t = t.sibling; t.tag !== 5 && t.tag !== 6 && t.tag !== 18; ) {
        if (t.tag === 27 && Hn(t.type) || t.flags & 2 || t.child === null || t.tag === 4) continue t;
        t.child.return = t, t = t.child;
      }
      if (!(t.flags & 2)) return t.stateNode;
    }
  }
  function tr(t, e, n) {
    var a = t.tag;
    if (a === 5 || a === 6)
      t = t.stateNode, e ? (n.nodeType === 9 ? n.body : n.nodeName === "HTML" ? n.ownerDocument.body : n).insertBefore(t, e) : (e = n.nodeType === 9 ? n.body : n.nodeName === "HTML" ? n.ownerDocument.body : n, e.appendChild(t), n = n._reactRootContainer, n != null || e.onclick !== null || (e.onclick = en));
    else if (a !== 4 && (a === 27 && Hn(t.type) && (n = t.stateNode, e = null), t = t.child, t !== null))
      for (tr(t, e, n), t = t.sibling; t !== null; )
        tr(t, e, n), t = t.sibling;
  }
  function ms(t, e, n) {
    var a = t.tag;
    if (a === 5 || a === 6)
      t = t.stateNode, e ? n.insertBefore(t, e) : n.appendChild(t);
    else if (a !== 4 && (a === 27 && Hn(t.type) && (n = t.stateNode), t = t.child, t !== null))
      for (ms(t, e, n), t = t.sibling; t !== null; )
        ms(t, e, n), t = t.sibling;
  }
  function Yd(t) {
    var e = t.stateNode, n = t.memoizedProps;
    try {
      for (var a = t.type, s = e.attributes; s.length; )
        e.removeAttributeNode(s[0]);
      ne(e, a, n), e[$t] = t, e[ce] = n;
    } catch (r) {
      xt(t, t.return, r);
    }
  }
  var hn = !1, Qt = !1, er = !1, qd = typeof WeakSet == "function" ? WeakSet : Set, Wt = null;
  function Qv(t, e) {
    if (t = t.containerInfo, Ar = Ns, t = If(t), Ju(t)) {
      if ("selectionStart" in t)
        var n = {
          start: t.selectionStart,
          end: t.selectionEnd
        };
      else
        t: {
          n = (n = t.ownerDocument) && n.defaultView || window;
          var a = n.getSelection && n.getSelection();
          if (a && a.rangeCount !== 0) {
            n = a.anchorNode;
            var s = a.anchorOffset, r = a.focusNode;
            a = a.focusOffset;
            try {
              n.nodeType, r.nodeType;
            } catch {
              n = null;
              break t;
            }
            var f = 0, p = -1, T = -1, D = 0, V = 0, B = t, C = null;
            e: for (; ; ) {
              for (var R; B !== n || s !== 0 && B.nodeType !== 3 || (p = f + s), B !== r || a !== 0 && B.nodeType !== 3 || (T = f + a), B.nodeType === 3 && (f += B.nodeValue.length), (R = B.firstChild) !== null; )
                C = B, B = R;
              for (; ; ) {
                if (B === t) break e;
                if (C === n && ++D === s && (p = f), C === r && ++V === a && (T = f), (R = B.nextSibling) !== null) break;
                B = C, C = B.parentNode;
              }
              B = R;
            }
            n = p === -1 || T === -1 ? null : { start: p, end: T };
          } else n = null;
        }
      n = n || { start: 0, end: 0 };
    } else n = null;
    for (Er = { focusedElem: t, selectionRange: n }, Ns = !1, Wt = e; Wt !== null; )
      if (e = Wt, t = e.child, (e.subtreeFlags & 1028) !== 0 && t !== null)
        t.return = e, Wt = t;
      else
        for (; Wt !== null; ) {
          switch (e = Wt, r = e.alternate, t = e.flags, e.tag) {
            case 0:
              if ((t & 4) !== 0 && (t = e.updateQueue, t = t !== null ? t.events : null, t !== null))
                for (n = 0; n < t.length; n++)
                  s = t[n], s.ref.impl = s.nextImpl;
              break;
            case 11:
            case 15:
              break;
            case 1:
              if ((t & 1024) !== 0 && r !== null) {
                t = void 0, n = e, s = r.memoizedProps, r = r.memoizedState, a = n.stateNode;
                try {
                  var k = fi(
                    n.type,
                    s
                  );
                  t = a.getSnapshotBeforeUpdate(
                    k,
                    r
                  ), a.__reactInternalSnapshotBeforeUpdate = t;
                } catch (et) {
                  xt(
                    n,
                    n.return,
                    et
                  );
                }
              }
              break;
            case 3:
              if ((t & 1024) !== 0) {
                if (t = e.stateNode.containerInfo, n = t.nodeType, n === 9)
                  Dr(t);
                else if (n === 1)
                  switch (t.nodeName) {
                    case "HEAD":
                    case "HTML":
                    case "BODY":
                      Dr(t);
                      break;
                    default:
                      t.textContent = "";
                  }
              }
              break;
            case 5:
            case 26:
            case 27:
            case 6:
            case 4:
            case 17:
              break;
            default:
              if ((t & 1024) !== 0) throw Error(o(163));
          }
          if (t = e.sibling, t !== null) {
            t.return = e.return, Wt = t;
            break;
          }
          Wt = e.return;
        }
  }
  function Gd(t, e, n) {
    var a = n.flags;
    switch (n.tag) {
      case 0:
      case 11:
      case 15:
        mn(t, n), a & 4 && Xa(5, n);
        break;
      case 1:
        if (mn(t, n), a & 4)
          if (t = n.stateNode, e === null)
            try {
              t.componentDidMount();
            } catch (f) {
              xt(n, n.return, f);
            }
          else {
            var s = fi(
              n.type,
              e.memoizedProps
            );
            e = e.memoizedState;
            try {
              t.componentDidUpdate(
                s,
                e,
                t.__reactInternalSnapshotBeforeUpdate
              );
            } catch (f) {
              xt(
                n,
                n.return,
                f
              );
            }
          }
        a & 64 && jd(n), a & 512 && Za(n, n.return);
        break;
      case 3:
        if (mn(t, n), a & 64 && (t = n.updateQueue, t !== null)) {
          if (e = null, n.child !== null)
            switch (n.child.tag) {
              case 27:
              case 5:
                e = n.child.stateNode;
                break;
              case 1:
                e = n.child.stateNode;
            }
          try {
            Dh(t, e);
          } catch (f) {
            xt(n, n.return, f);
          }
        }
        break;
      case 27:
        e === null && a & 4 && Yd(n);
      case 26:
      case 5:
        mn(t, n), e === null && a & 4 && Ld(n), a & 512 && Za(n, n.return);
        break;
      case 12:
        mn(t, n);
        break;
      case 31:
        mn(t, n), a & 4 && Qd(t, n);
        break;
      case 13:
        mn(t, n), a & 4 && Kd(t, n), a & 64 && (t = n.memoizedState, t !== null && (t = t.dehydrated, t !== null && (n = t1.bind(
          null,
          n
        ), T1(t, n))));
        break;
      case 22:
        if (a = n.memoizedState !== null || hn, !a) {
          e = e !== null && e.memoizedState !== null || Qt, s = hn;
          var r = Qt;
          hn = a, (Qt = e) && !r ? yn(
            t,
            n,
            (n.subtreeFlags & 8772) !== 0
          ) : mn(t, n), hn = s, Qt = r;
        }
        break;
      case 30:
        break;
      default:
        mn(t, n);
    }
  }
  function Xd(t) {
    var e = t.alternate;
    e !== null && (t.alternate = null, Xd(e)), t.child = null, t.deletions = null, t.sibling = null, t.tag === 5 && (e = t.stateNode, e !== null && Ou(e)), t.stateNode = null, t.return = null, t.dependencies = null, t.memoizedProps = null, t.memoizedState = null, t.pendingProps = null, t.stateNode = null, t.updateQueue = null;
  }
  var Ut = null, he = !1;
  function dn(t, e, n) {
    for (n = n.child; n !== null; )
      Zd(t, e, n), n = n.sibling;
  }
  function Zd(t, e, n) {
    if (ve && typeof ve.onCommitFiberUnmount == "function")
      try {
        ve.onCommitFiberUnmount(ma, n);
      } catch {
      }
    switch (n.tag) {
      case 26:
        Qt || ke(n, e), dn(
          t,
          e,
          n
        ), n.memoizedState ? n.memoizedState.count-- : n.stateNode && (n = n.stateNode, n.parentNode.removeChild(n));
        break;
      case 27:
        Qt || ke(n, e);
        var a = Ut, s = he;
        Hn(n.type) && (Ut = n.stateNode, he = !1), dn(
          t,
          e,
          n
        ), Ia(n.stateNode), Ut = a, he = s;
        break;
      case 5:
        Qt || ke(n, e);
      case 6:
        if (a = Ut, s = he, Ut = null, dn(
          t,
          e,
          n
        ), Ut = a, he = s, Ut !== null)
          if (he)
            try {
              (Ut.nodeType === 9 ? Ut.body : Ut.nodeName === "HTML" ? Ut.ownerDocument.body : Ut).removeChild(n.stateNode);
            } catch (r) {
              xt(
                n,
                e,
                r
              );
            }
          else
            try {
              Ut.removeChild(n.stateNode);
            } catch (r) {
              xt(
                n,
                e,
                r
              );
            }
        break;
      case 18:
        Ut !== null && (he ? (t = Ut, jm(
          t.nodeType === 9 ? t.body : t.nodeName === "HTML" ? t.ownerDocument.body : t,
          n.stateNode
        ), ia(t)) : jm(Ut, n.stateNode));
        break;
      case 4:
        a = Ut, s = he, Ut = n.stateNode.containerInfo, he = !0, dn(
          t,
          e,
          n
        ), Ut = a, he = s;
        break;
      case 0:
      case 11:
      case 14:
      case 15:
        _n(2, n, e), Qt || _n(4, n, e), dn(
          t,
          e,
          n
        );
        break;
      case 1:
        Qt || (ke(n, e), a = n.stateNode, typeof a.componentWillUnmount == "function" && wd(
          n,
          e,
          a
        )), dn(
          t,
          e,
          n
        );
        break;
      case 21:
        dn(
          t,
          e,
          n
        );
        break;
      case 22:
        Qt = (a = Qt) || n.memoizedState !== null, dn(
          t,
          e,
          n
        ), Qt = a;
        break;
      default:
        dn(
          t,
          e,
          n
        );
    }
  }
  function Qd(t, e) {
    if (e.memoizedState === null && (t = e.alternate, t !== null && (t = t.memoizedState, t !== null))) {
      t = t.dehydrated;
      try {
        ia(t);
      } catch (n) {
        xt(e, e.return, n);
      }
    }
  }
  function Kd(t, e) {
    if (e.memoizedState === null && (t = e.alternate, t !== null && (t = t.memoizedState, t !== null && (t = t.dehydrated, t !== null))))
      try {
        ia(t);
      } catch (n) {
        xt(e, e.return, n);
      }
  }
  function Kv(t) {
    switch (t.tag) {
      case 31:
      case 13:
      case 19:
        var e = t.stateNode;
        return e === null && (e = t.stateNode = new qd()), e;
      case 22:
        return t = t.stateNode, e = t._retryCache, e === null && (e = t._retryCache = new qd()), e;
      default:
        throw Error(o(435, t.tag));
    }
  }
  function ys(t, e) {
    var n = Kv(t);
    e.forEach(function(a) {
      if (!n.has(a)) {
        n.add(a);
        var s = e1.bind(null, t, a);
        a.then(s, s);
      }
    });
  }
  function de(t, e) {
    var n = e.deletions;
    if (n !== null)
      for (var a = 0; a < n.length; a++) {
        var s = n[a], r = t, f = e, p = f;
        t: for (; p !== null; ) {
          switch (p.tag) {
            case 27:
              if (Hn(p.type)) {
                Ut = p.stateNode, he = !1;
                break t;
              }
              break;
            case 5:
              Ut = p.stateNode, he = !1;
              break t;
            case 3:
            case 4:
              Ut = p.stateNode.containerInfo, he = !0;
              break t;
          }
          p = p.return;
        }
        if (Ut === null) throw Error(o(160));
        Zd(r, f, s), Ut = null, he = !1, r = s.alternate, r !== null && (r.return = null), s.return = null;
      }
    if (e.subtreeFlags & 13886)
      for (e = e.child; e !== null; )
        Jd(e, t), e = e.sibling;
  }
  var qe = null;
  function Jd(t, e) {
    var n = t.alternate, a = t.flags;
    switch (t.tag) {
      case 0:
      case 11:
      case 14:
      case 15:
        de(e, t), me(t), a & 4 && (_n(3, t, t.return), Xa(3, t), _n(5, t, t.return));
        break;
      case 1:
        de(e, t), me(t), a & 512 && (Qt || n === null || ke(n, n.return)), a & 64 && hn && (t = t.updateQueue, t !== null && (a = t.callbacks, a !== null && (n = t.shared.hiddenCallbacks, t.shared.hiddenCallbacks = n === null ? a : n.concat(a))));
        break;
      case 26:
        var s = qe;
        if (de(e, t), me(t), a & 512 && (Qt || n === null || ke(n, n.return)), a & 4) {
          var r = n !== null ? n.memoizedState : null;
          if (a = t.memoizedState, n === null)
            if (a === null)
              if (t.stateNode === null) {
                t: {
                  a = t.type, n = t.memoizedProps, s = s.ownerDocument || s;
                  e: switch (a) {
                    case "title":
                      r = s.getElementsByTagName("title")[0], (!r || r[ga] || r[$t] || r.namespaceURI === "http://www.w3.org/2000/svg" || r.hasAttribute("itemprop")) && (r = s.createElement(a), s.head.insertBefore(
                        r,
                        s.querySelector("head > title")
                      )), ne(r, a, n), r[$t] = t, Ft(r), a = r;
                      break t;
                    case "link":
                      var f = Jm(
                        "link",
                        "href",
                        s
                      ).get(a + (n.href || ""));
                      if (f) {
                        for (var p = 0; p < f.length; p++)
                          if (r = f[p], r.getAttribute("href") === (n.href == null || n.href === "" ? null : n.href) && r.getAttribute("rel") === (n.rel == null ? null : n.rel) && r.getAttribute("title") === (n.title == null ? null : n.title) && r.getAttribute("crossorigin") === (n.crossOrigin == null ? null : n.crossOrigin)) {
                            f.splice(p, 1);
                            break e;
                          }
                      }
                      r = s.createElement(a), ne(r, a, n), s.head.appendChild(r);
                      break;
                    case "meta":
                      if (f = Jm(
                        "meta",
                        "content",
                        s
                      ).get(a + (n.content || ""))) {
                        for (p = 0; p < f.length; p++)
                          if (r = f[p], r.getAttribute("content") === (n.content == null ? null : "" + n.content) && r.getAttribute("name") === (n.name == null ? null : n.name) && r.getAttribute("property") === (n.property == null ? null : n.property) && r.getAttribute("http-equiv") === (n.httpEquiv == null ? null : n.httpEquiv) && r.getAttribute("charset") === (n.charSet == null ? null : n.charSet)) {
                            f.splice(p, 1);
                            break e;
                          }
                      }
                      r = s.createElement(a), ne(r, a, n), s.head.appendChild(r);
                      break;
                    default:
                      throw Error(o(468, a));
                  }
                  r[$t] = t, Ft(r), a = r;
                }
                t.stateNode = a;
              } else
                km(
                  s,
                  t.type,
                  t.stateNode
                );
            else
              t.stateNode = Km(
                s,
                a,
                t.memoizedProps
              );
          else
            r !== a ? (r === null ? n.stateNode !== null && (n = n.stateNode, n.parentNode.removeChild(n)) : r.count--, a === null ? km(
              s,
              t.type,
              t.stateNode
            ) : Km(
              s,
              a,
              t.memoizedProps
            )) : a === null && t.stateNode !== null && $o(
              t,
              t.memoizedProps,
              n.memoizedProps
            );
        }
        break;
      case 27:
        de(e, t), me(t), a & 512 && (Qt || n === null || ke(n, n.return)), n !== null && a & 4 && $o(
          t,
          t.memoizedProps,
          n.memoizedProps
        );
        break;
      case 5:
        if (de(e, t), me(t), a & 512 && (Qt || n === null || ke(n, n.return)), t.flags & 32) {
          s = t.stateNode;
          try {
            Di(s, "");
          } catch (k) {
            xt(t, t.return, k);
          }
        }
        a & 4 && t.stateNode != null && (s = t.memoizedProps, $o(
          t,
          s,
          n !== null ? n.memoizedProps : s
        )), a & 1024 && (er = !0);
        break;
      case 6:
        if (de(e, t), me(t), a & 4) {
          if (t.stateNode === null)
            throw Error(o(162));
          a = t.memoizedProps, n = t.stateNode;
          try {
            n.nodeValue = a;
          } catch (k) {
            xt(t, t.return, k);
          }
        }
        break;
      case 3:
        if (Vs = null, s = qe, qe = Rs(e.containerInfo), de(e, t), qe = s, me(t), a & 4 && n !== null && n.memoizedState.isDehydrated)
          try {
            ia(e.containerInfo);
          } catch (k) {
            xt(t, t.return, k);
          }
        er && (er = !1, kd(t));
        break;
      case 4:
        a = qe, qe = Rs(
          t.stateNode.containerInfo
        ), de(e, t), me(t), qe = a;
        break;
      case 12:
        de(e, t), me(t);
        break;
      case 31:
        de(e, t), me(t), a & 4 && (a = t.updateQueue, a !== null && (t.updateQueue = null, ys(t, a)));
        break;
      case 13:
        de(e, t), me(t), t.child.flags & 8192 && t.memoizedState !== null != (n !== null && n.memoizedState !== null) && (gs = ge()), a & 4 && (a = t.updateQueue, a !== null && (t.updateQueue = null, ys(t, a)));
        break;
      case 22:
        s = t.memoizedState !== null;
        var T = n !== null && n.memoizedState !== null, D = hn, V = Qt;
        if (hn = D || s, Qt = V || T, de(e, t), Qt = V, hn = D, me(t), a & 8192)
          t: for (e = t.stateNode, e._visibility = s ? e._visibility & -2 : e._visibility | 1, s && (n === null || T || hn || Qt || hi(t)), n = null, e = t; ; ) {
            if (e.tag === 5 || e.tag === 26) {
              if (n === null) {
                T = n = e;
                try {
                  if (r = T.stateNode, s)
                    f = r.style, typeof f.setProperty == "function" ? f.setProperty("display", "none", "important") : f.display = "none";
                  else {
                    p = T.stateNode;
                    var B = T.memoizedProps.style, C = B != null && B.hasOwnProperty("display") ? B.display : null;
                    p.style.display = C == null || typeof C == "boolean" ? "" : ("" + C).trim();
                  }
                } catch (k) {
                  xt(T, T.return, k);
                }
              }
            } else if (e.tag === 6) {
              if (n === null) {
                T = e;
                try {
                  T.stateNode.nodeValue = s ? "" : T.memoizedProps;
                } catch (k) {
                  xt(T, T.return, k);
                }
              }
            } else if (e.tag === 18) {
              if (n === null) {
                T = e;
                try {
                  var R = T.stateNode;
                  s ? wm(R, !0) : wm(T.stateNode, !1);
                } catch (k) {
                  xt(T, T.return, k);
                }
              }
            } else if ((e.tag !== 22 && e.tag !== 23 || e.memoizedState === null || e === t) && e.child !== null) {
              e.child.return = e, e = e.child;
              continue;
            }
            if (e === t) break t;
            for (; e.sibling === null; ) {
              if (e.return === null || e.return === t) break t;
              n === e && (n = null), e = e.return;
            }
            n === e && (n = null), e.sibling.return = e.return, e = e.sibling;
          }
        a & 4 && (a = t.updateQueue, a !== null && (n = a.retryQueue, n !== null && (a.retryQueue = null, ys(t, n))));
        break;
      case 19:
        de(e, t), me(t), a & 4 && (a = t.updateQueue, a !== null && (t.updateQueue = null, ys(t, a)));
        break;
      case 30:
        break;
      case 21:
        break;
      default:
        de(e, t), me(t);
    }
  }
  function me(t) {
    var e = t.flags;
    if (e & 2) {
      try {
        for (var n, a = t.return; a !== null; ) {
          if (Hd(a)) {
            n = a;
            break;
          }
          a = a.return;
        }
        if (n == null) throw Error(o(160));
        switch (n.tag) {
          case 27:
            var s = n.stateNode, r = Io(t);
            ms(t, r, s);
            break;
          case 5:
            var f = n.stateNode;
            n.flags & 32 && (Di(f, ""), n.flags &= -33);
            var p = Io(t);
            ms(t, p, f);
            break;
          case 3:
          case 4:
            var T = n.stateNode.containerInfo, D = Io(t);
            tr(
              t,
              D,
              T
            );
            break;
          default:
            throw Error(o(161));
        }
      } catch (V) {
        xt(t, t.return, V);
      }
      t.flags &= -3;
    }
    e & 4096 && (t.flags &= -4097);
  }
  function kd(t) {
    if (t.subtreeFlags & 1024)
      for (t = t.child; t !== null; ) {
        var e = t;
        kd(e), e.tag === 5 && e.flags & 1024 && e.stateNode.reset(), t = t.sibling;
      }
  }
  function mn(t, e) {
    if (e.subtreeFlags & 8772)
      for (e = e.child; e !== null; )
        Gd(t, e.alternate, e), e = e.sibling;
  }
  function hi(t) {
    for (t = t.child; t !== null; ) {
      var e = t;
      switch (e.tag) {
        case 0:
        case 11:
        case 14:
        case 15:
          _n(4, e, e.return), hi(e);
          break;
        case 1:
          ke(e, e.return);
          var n = e.stateNode;
          typeof n.componentWillUnmount == "function" && wd(
            e,
            e.return,
            n
          ), hi(e);
          break;
        case 27:
          Ia(e.stateNode);
        case 26:
        case 5:
          ke(e, e.return), hi(e);
          break;
        case 22:
          e.memoizedState === null && hi(e);
          break;
        case 30:
          hi(e);
          break;
        default:
          hi(e);
      }
      t = t.sibling;
    }
  }
  function yn(t, e, n) {
    for (n = n && (e.subtreeFlags & 8772) !== 0, e = e.child; e !== null; ) {
      var a = e.alternate, s = t, r = e, f = r.flags;
      switch (r.tag) {
        case 0:
        case 11:
        case 15:
          yn(
            s,
            r,
            n
          ), Xa(4, r);
          break;
        case 1:
          if (yn(
            s,
            r,
            n
          ), a = r, s = a.stateNode, typeof s.componentDidMount == "function")
            try {
              s.componentDidMount();
            } catch (D) {
              xt(a, a.return, D);
            }
          if (a = r, s = a.updateQueue, s !== null) {
            var p = a.stateNode;
            try {
              var T = s.shared.hiddenCallbacks;
              if (T !== null)
                for (s.shared.hiddenCallbacks = null, s = 0; s < T.length; s++)
                  Mh(T[s], p);
            } catch (D) {
              xt(a, a.return, D);
            }
          }
          n && f & 64 && jd(r), Za(r, r.return);
          break;
        case 27:
          Yd(r);
        case 26:
        case 5:
          yn(
            s,
            r,
            n
          ), n && a === null && f & 4 && Ld(r), Za(r, r.return);
          break;
        case 12:
          yn(
            s,
            r,
            n
          );
          break;
        case 31:
          yn(
            s,
            r,
            n
          ), n && f & 4 && Qd(s, r);
          break;
        case 13:
          yn(
            s,
            r,
            n
          ), n && f & 4 && Kd(s, r);
          break;
        case 22:
          r.memoizedState === null && yn(
            s,
            r,
            n
          ), Za(r, r.return);
          break;
        case 30:
          break;
        default:
          yn(
            s,
            r,
            n
          );
      }
      e = e.sibling;
    }
  }
  function nr(t, e) {
    var n = null;
    t !== null && t.memoizedState !== null && t.memoizedState.cachePool !== null && (n = t.memoizedState.cachePool.pool), t = null, e.memoizedState !== null && e.memoizedState.cachePool !== null && (t = e.memoizedState.cachePool.pool), t !== n && (t != null && t.refCount++, n != null && Oa(n));
  }
  function ir(t, e) {
    t = null, e.alternate !== null && (t = e.alternate.memoizedState.cache), e = e.memoizedState.cache, e !== t && (e.refCount++, t != null && Oa(t));
  }
  function Ge(t, e, n, a) {
    if (e.subtreeFlags & 10256)
      for (e = e.child; e !== null; )
        Fd(
          t,
          e,
          n,
          a
        ), e = e.sibling;
  }
  function Fd(t, e, n, a) {
    var s = e.flags;
    switch (e.tag) {
      case 0:
      case 11:
      case 15:
        Ge(
          t,
          e,
          n,
          a
        ), s & 2048 && Xa(9, e);
        break;
      case 1:
        Ge(
          t,
          e,
          n,
          a
        );
        break;
      case 3:
        Ge(
          t,
          e,
          n,
          a
        ), s & 2048 && (t = null, e.alternate !== null && (t = e.alternate.memoizedState.cache), e = e.memoizedState.cache, e !== t && (e.refCount++, t != null && Oa(t)));
        break;
      case 12:
        if (s & 2048) {
          Ge(
            t,
            e,
            n,
            a
          ), t = e.stateNode;
          try {
            var r = e.memoizedProps, f = r.id, p = r.onPostCommit;
            typeof p == "function" && p(
              f,
              e.alternate === null ? "mount" : "update",
              t.passiveEffectDuration,
              -0
            );
          } catch (T) {
            xt(e, e.return, T);
          }
        } else
          Ge(
            t,
            e,
            n,
            a
          );
        break;
      case 31:
        Ge(
          t,
          e,
          n,
          a
        );
        break;
      case 13:
        Ge(
          t,
          e,
          n,
          a
        );
        break;
      case 23:
        break;
      case 22:
        r = e.stateNode, f = e.alternate, e.memoizedState !== null ? r._visibility & 2 ? Ge(
          t,
          e,
          n,
          a
        ) : Qa(t, e) : r._visibility & 2 ? Ge(
          t,
          e,
          n,
          a
        ) : (r._visibility |= 2, Ki(
          t,
          e,
          n,
          a,
          (e.subtreeFlags & 10256) !== 0 || !1
        )), s & 2048 && nr(f, e);
        break;
      case 24:
        Ge(
          t,
          e,
          n,
          a
        ), s & 2048 && ir(e.alternate, e);
        break;
      default:
        Ge(
          t,
          e,
          n,
          a
        );
    }
  }
  function Ki(t, e, n, a, s) {
    for (s = s && ((e.subtreeFlags & 10256) !== 0 || !1), e = e.child; e !== null; ) {
      var r = t, f = e, p = n, T = a, D = f.flags;
      switch (f.tag) {
        case 0:
        case 11:
        case 15:
          Ki(
            r,
            f,
            p,
            T,
            s
          ), Xa(8, f);
          break;
        case 23:
          break;
        case 22:
          var V = f.stateNode;
          f.memoizedState !== null ? V._visibility & 2 ? Ki(
            r,
            f,
            p,
            T,
            s
          ) : Qa(
            r,
            f
          ) : (V._visibility |= 2, Ki(
            r,
            f,
            p,
            T,
            s
          )), s && D & 2048 && nr(
            f.alternate,
            f
          );
          break;
        case 24:
          Ki(
            r,
            f,
            p,
            T,
            s
          ), s && D & 2048 && ir(f.alternate, f);
          break;
        default:
          Ki(
            r,
            f,
            p,
            T,
            s
          );
      }
      e = e.sibling;
    }
  }
  function Qa(t, e) {
    if (e.subtreeFlags & 10256)
      for (e = e.child; e !== null; ) {
        var n = t, a = e, s = a.flags;
        switch (a.tag) {
          case 22:
            Qa(n, a), s & 2048 && nr(
              a.alternate,
              a
            );
            break;
          case 24:
            Qa(n, a), s & 2048 && ir(a.alternate, a);
            break;
          default:
            Qa(n, a);
        }
        e = e.sibling;
      }
  }
  var Ka = 8192;
  function Ji(t, e, n) {
    if (t.subtreeFlags & Ka)
      for (t = t.child; t !== null; )
        Wd(
          t,
          e,
          n
        ), t = t.sibling;
  }
  function Wd(t, e, n) {
    switch (t.tag) {
      case 26:
        Ji(
          t,
          e,
          n
        ), t.flags & Ka && t.memoizedState !== null && _1(
          n,
          qe,
          t.memoizedState,
          t.memoizedProps
        );
        break;
      case 5:
        Ji(
          t,
          e,
          n
        );
        break;
      case 3:
      case 4:
        var a = qe;
        qe = Rs(t.stateNode.containerInfo), Ji(
          t,
          e,
          n
        ), qe = a;
        break;
      case 22:
        t.memoizedState === null && (a = t.alternate, a !== null && a.memoizedState !== null ? (a = Ka, Ka = 16777216, Ji(
          t,
          e,
          n
        ), Ka = a) : Ji(
          t,
          e,
          n
        ));
        break;
      default:
        Ji(
          t,
          e,
          n
        );
    }
  }
  function Pd(t) {
    var e = t.alternate;
    if (e !== null && (t = e.child, t !== null)) {
      e.child = null;
      do
        e = t.sibling, t.sibling = null, t = e;
      while (t !== null);
    }
  }
  function Ja(t) {
    var e = t.deletions;
    if ((t.flags & 16) !== 0) {
      if (e !== null)
        for (var n = 0; n < e.length; n++) {
          var a = e[n];
          Wt = a, Id(
            a,
            t
          );
        }
      Pd(t);
    }
    if (t.subtreeFlags & 10256)
      for (t = t.child; t !== null; )
        $d(t), t = t.sibling;
  }
  function $d(t) {
    switch (t.tag) {
      case 0:
      case 11:
      case 15:
        Ja(t), t.flags & 2048 && _n(9, t, t.return);
        break;
      case 3:
        Ja(t);
        break;
      case 12:
        Ja(t);
        break;
      case 22:
        var e = t.stateNode;
        t.memoizedState !== null && e._visibility & 2 && (t.return === null || t.return.tag !== 13) ? (e._visibility &= -3, ps(t)) : Ja(t);
        break;
      default:
        Ja(t);
    }
  }
  function ps(t) {
    var e = t.deletions;
    if ((t.flags & 16) !== 0) {
      if (e !== null)
        for (var n = 0; n < e.length; n++) {
          var a = e[n];
          Wt = a, Id(
            a,
            t
          );
        }
      Pd(t);
    }
    for (t = t.child; t !== null; ) {
      switch (e = t, e.tag) {
        case 0:
        case 11:
        case 15:
          _n(8, e, e.return), ps(e);
          break;
        case 22:
          n = e.stateNode, n._visibility & 2 && (n._visibility &= -3, ps(e));
          break;
        default:
          ps(e);
      }
      t = t.sibling;
    }
  }
  function Id(t, e) {
    for (; Wt !== null; ) {
      var n = Wt;
      switch (n.tag) {
        case 0:
        case 11:
        case 15:
          _n(8, n, e);
          break;
        case 23:
        case 22:
          if (n.memoizedState !== null && n.memoizedState.cachePool !== null) {
            var a = n.memoizedState.cachePool.pool;
            a != null && a.refCount++;
          }
          break;
        case 24:
          Oa(n.memoizedState.cache);
      }
      if (a = n.child, a !== null) a.return = n, Wt = a;
      else
        t: for (n = t; Wt !== null; ) {
          a = Wt;
          var s = a.sibling, r = a.return;
          if (Xd(a), a === n) {
            Wt = null;
            break t;
          }
          if (s !== null) {
            s.return = r, Wt = s;
            break t;
          }
          Wt = r;
        }
    }
  }
  var Jv = {
    getCacheForType: function(t) {
      var e = te(Gt), n = e.data.get(t);
      return n === void 0 && (n = t(), e.data.set(t, n)), n;
    },
    cacheSignal: function() {
      return te(Gt).controller.signal;
    }
  }, kv = typeof WeakMap == "function" ? WeakMap : Map, bt = 0, zt = null, ft = null, dt = 0, Et = 0, xe = null, Un = !1, ki = !1, ar = !1, pn = 0, Nt = 0, Bn = 0, di = 0, lr = 0, Me = 0, Fi = 0, ka = null, ye = null, sr = !1, gs = 0, tm = 0, vs = 1 / 0, Ss = null, Nn = null, Jt = 0, jn = null, Wi = null, gn = 0, ur = 0, or = null, em = null, Fa = 0, rr = null;
  function De() {
    return (bt & 2) !== 0 && dt !== 0 ? dt & -dt : O.T !== null ? yr() : gf();
  }
  function nm() {
    if (Me === 0)
      if ((dt & 536870912) === 0 || gt) {
        var t = Cl;
        Cl <<= 1, (Cl & 3932160) === 0 && (Cl = 262144), Me = t;
      } else Me = 536870912;
    return t = Ae.current, t !== null && (t.flags |= 32), Me;
  }
  function pe(t, e, n) {
    (t === zt && (Et === 2 || Et === 9) || t.cancelPendingCommit !== null) && (Pi(t, 0), wn(
      t,
      dt,
      Me,
      !1
    )), pa(t, n), ((bt & 2) === 0 || t !== zt) && (t === zt && ((bt & 2) === 0 && (di |= n), Nt === 4 && wn(
      t,
      dt,
      Me,
      !1
    )), Fe(t));
  }
  function im(t, e, n) {
    if ((bt & 6) !== 0) throw Error(o(327));
    var a = !n && (e & 127) === 0 && (e & t.expiredLanes) === 0 || ya(t, e), s = a ? Pv(t, e) : fr(t, e, !0), r = a;
    do {
      if (s === 0) {
        ki && !a && wn(t, e, 0, !1);
        break;
      } else {
        if (n = t.current.alternate, r && !Fv(n)) {
          s = fr(t, e, !1), r = !1;
          continue;
        }
        if (s === 2) {
          if (r = e, t.errorRecoveryDisabledLanes & r)
            var f = 0;
          else
            f = t.pendingLanes & -536870913, f = f !== 0 ? f : f & 536870912 ? 536870912 : 0;
          if (f !== 0) {
            e = f;
            t: {
              var p = t;
              s = ka;
              var T = p.current.memoizedState.isDehydrated;
              if (T && (Pi(p, f).flags |= 256), f = fr(
                p,
                f,
                !1
              ), f !== 2) {
                if (ar && !T) {
                  p.errorRecoveryDisabledLanes |= r, di |= r, s = 4;
                  break t;
                }
                r = ye, ye = s, r !== null && (ye === null ? ye = r : ye.push.apply(
                  ye,
                  r
                ));
              }
              s = f;
            }
            if (r = !1, s !== 2) continue;
          }
        }
        if (s === 1) {
          Pi(t, 0), wn(t, e, 0, !0);
          break;
        }
        t: {
          switch (a = t, r = s, r) {
            case 0:
            case 1:
              throw Error(o(345));
            case 4:
              if ((e & 4194048) !== e) break;
            case 6:
              wn(
                a,
                e,
                Me,
                !Un
              );
              break t;
            case 2:
              ye = null;
              break;
            case 3:
            case 5:
              break;
            default:
              throw Error(o(329));
          }
          if ((e & 62914560) === e && (s = gs + 300 - ge(), 10 < s)) {
            if (wn(
              a,
              e,
              Me,
              !Un
            ), Rl(a, 0, !0) !== 0) break t;
            gn = e, a.timeoutHandle = Bm(
              am.bind(
                null,
                a,
                n,
                ye,
                Ss,
                sr,
                e,
                Me,
                di,
                Fi,
                Un,
                r,
                "Throttled",
                -0,
                0
              ),
              s
            );
            break t;
          }
          am(
            a,
            n,
            ye,
            Ss,
            sr,
            e,
            Me,
            di,
            Fi,
            Un,
            r,
            null,
            -0,
            0
          );
        }
      }
      break;
    } while (!0);
    Fe(t);
  }
  function am(t, e, n, a, s, r, f, p, T, D, V, B, C, R) {
    if (t.timeoutHandle = -1, B = e.subtreeFlags, B & 8192 || (B & 16785408) === 16785408) {
      B = {
        stylesheets: null,
        count: 0,
        imgCount: 0,
        imgBytes: 0,
        suspenseyImages: [],
        waitingForImages: !0,
        waitingForViewTransition: !1,
        unsuspend: en
      }, Wd(
        e,
        r,
        B
      );
      var k = (r & 62914560) === r ? gs - ge() : (r & 4194048) === r ? tm - ge() : 0;
      if (k = U1(
        B,
        k
      ), k !== null) {
        gn = r, t.cancelPendingCommit = k(
          hm.bind(
            null,
            t,
            e,
            r,
            n,
            a,
            s,
            f,
            p,
            T,
            V,
            B,
            null,
            C,
            R
          )
        ), wn(t, r, f, !D);
        return;
      }
    }
    hm(
      t,
      e,
      r,
      n,
      a,
      s,
      f,
      p,
      T
    );
  }
  function Fv(t) {
    for (var e = t; ; ) {
      var n = e.tag;
      if ((n === 0 || n === 11 || n === 15) && e.flags & 16384 && (n = e.updateQueue, n !== null && (n = n.stores, n !== null)))
        for (var a = 0; a < n.length; a++) {
          var s = n[a], r = s.getSnapshot;
          s = s.value;
          try {
            if (!Te(r(), s)) return !1;
          } catch {
            return !1;
          }
        }
      if (n = e.child, e.subtreeFlags & 16384 && n !== null)
        n.return = e, e = n;
      else {
        if (e === t) break;
        for (; e.sibling === null; ) {
          if (e.return === null || e.return === t) return !0;
          e = e.return;
        }
        e.sibling.return = e.return, e = e.sibling;
      }
    }
    return !0;
  }
  function wn(t, e, n, a) {
    e &= ~lr, e &= ~di, t.suspendedLanes |= e, t.pingedLanes &= ~e, a && (t.warmLanes |= e), a = t.expirationTimes;
    for (var s = e; 0 < s; ) {
      var r = 31 - Se(s), f = 1 << r;
      a[r] = -1, s &= ~f;
    }
    n !== 0 && mf(t, n, e);
  }
  function Ts() {
    return (bt & 6) === 0 ? (Wa(0), !1) : !0;
  }
  function cr() {
    if (ft !== null) {
      if (Et === 0)
        var t = ft.return;
      else
        t = ft, sn = ai = null, Do(t), qi = null, _a = 0, t = ft;
      for (; t !== null; )
        Nd(t.alternate, t), t = t.return;
      ft = null;
    }
  }
  function Pi(t, e) {
    var n = t.timeoutHandle;
    n !== -1 && (t.timeoutHandle = -1, y1(n)), n = t.cancelPendingCommit, n !== null && (t.cancelPendingCommit = null, n()), gn = 0, cr(), zt = t, ft = n = an(t.current, null), dt = e, Et = 0, xe = null, Un = !1, ki = ya(t, e), ar = !1, Fi = Me = lr = di = Bn = Nt = 0, ye = ka = null, sr = !1, (e & 8) !== 0 && (e |= e & 32);
    var a = t.entangledLanes;
    if (a !== 0)
      for (t = t.entanglements, a &= e; 0 < a; ) {
        var s = 31 - Se(a), r = 1 << s;
        e |= t[s], a &= ~r;
      }
    return pn = e, ql(), n;
  }
  function lm(t, e) {
    st = null, O.H = Ya, e === Yi || e === Fl ? (e = bh(), Et = 3) : e === mo ? (e = bh(), Et = 4) : Et = e === Go ? 8 : e !== null && typeof e == "object" && typeof e.then == "function" ? 6 : 1, xe = e, ft === null && (Nt = 1, rs(
      t,
      Ve(e, t.current)
    ));
  }
  function sm() {
    var t = Ae.current;
    return t === null ? !0 : (dt & 4194048) === dt ? Ne === null : (dt & 62914560) === dt || (dt & 536870912) !== 0 ? t === Ne : !1;
  }
  function um() {
    var t = O.H;
    return O.H = Ya, t === null ? Ya : t;
  }
  function om() {
    var t = O.A;
    return O.A = Jv, t;
  }
  function bs() {
    Nt = 4, Un || (dt & 4194048) !== dt && Ae.current !== null || (ki = !0), (Bn & 134217727) === 0 && (di & 134217727) === 0 || zt === null || wn(
      zt,
      dt,
      Me,
      !1
    );
  }
  function fr(t, e, n) {
    var a = bt;
    bt |= 2;
    var s = um(), r = om();
    (zt !== t || dt !== e) && (Ss = null, Pi(t, e)), e = !1;
    var f = Nt;
    t: do
      try {
        if (Et !== 0 && ft !== null) {
          var p = ft, T = xe;
          switch (Et) {
            case 8:
              cr(), f = 6;
              break t;
            case 3:
            case 2:
            case 9:
            case 6:
              Ae.current === null && (e = !0);
              var D = Et;
              if (Et = 0, xe = null, $i(t, p, T, D), n && ki) {
                f = 0;
                break t;
              }
              break;
            default:
              D = Et, Et = 0, xe = null, $i(t, p, T, D);
          }
        }
        Wv(), f = Nt;
        break;
      } catch (V) {
        lm(t, V);
      }
    while (!0);
    return e && t.shellSuspendCounter++, sn = ai = null, bt = a, O.H = s, O.A = r, ft === null && (zt = null, dt = 0, ql()), f;
  }
  function Wv() {
    for (; ft !== null; ) rm(ft);
  }
  function Pv(t, e) {
    var n = bt;
    bt |= 2;
    var a = um(), s = om();
    zt !== t || dt !== e ? (Ss = null, vs = ge() + 500, Pi(t, e)) : ki = ya(
      t,
      e
    );
    t: do
      try {
        if (Et !== 0 && ft !== null) {
          e = ft;
          var r = xe;
          e: switch (Et) {
            case 1:
              Et = 0, xe = null, $i(t, e, r, 1);
              break;
            case 2:
            case 9:
              if (Sh(r)) {
                Et = 0, xe = null, cm(e);
                break;
              }
              e = function() {
                Et !== 2 && Et !== 9 || zt !== t || (Et = 7), Fe(t);
              }, r.then(e, e);
              break t;
            case 3:
              Et = 7;
              break t;
            case 4:
              Et = 5;
              break t;
            case 7:
              Sh(r) ? (Et = 0, xe = null, cm(e)) : (Et = 0, xe = null, $i(t, e, r, 7));
              break;
            case 5:
              var f = null;
              switch (ft.tag) {
                case 26:
                  f = ft.memoizedState;
                case 5:
                case 27:
                  var p = ft;
                  if (f ? Fm(f) : p.stateNode.complete) {
                    Et = 0, xe = null;
                    var T = p.sibling;
                    if (T !== null) ft = T;
                    else {
                      var D = p.return;
                      D !== null ? (ft = D, As(D)) : ft = null;
                    }
                    break e;
                  }
              }
              Et = 0, xe = null, $i(t, e, r, 5);
              break;
            case 6:
              Et = 0, xe = null, $i(t, e, r, 6);
              break;
            case 8:
              cr(), Nt = 6;
              break t;
            default:
              throw Error(o(462));
          }
        }
        $v();
        break;
      } catch (V) {
        lm(t, V);
      }
    while (!0);
    return sn = ai = null, O.H = a, O.A = s, bt = n, ft !== null ? 0 : (zt = null, dt = 0, ql(), Nt);
  }
  function $v() {
    for (; ft !== null && !b0(); )
      rm(ft);
  }
  function rm(t) {
    var e = Ud(t.alternate, t, pn);
    t.memoizedProps = t.pendingProps, e === null ? As(t) : ft = e;
  }
  function cm(t) {
    var e = t, n = e.alternate;
    switch (e.tag) {
      case 15:
      case 0:
        e = Cd(
          n,
          e,
          e.pendingProps,
          e.type,
          void 0,
          dt
        );
        break;
      case 11:
        e = Cd(
          n,
          e,
          e.pendingProps,
          e.type.render,
          e.ref,
          dt
        );
        break;
      case 5:
        Do(e);
      default:
        Nd(n, e), e = ft = oh(e, pn), e = Ud(n, e, pn);
    }
    t.memoizedProps = t.pendingProps, e === null ? As(t) : ft = e;
  }
  function $i(t, e, n, a) {
    sn = ai = null, Do(e), qi = null, _a = 0;
    var s = e.return;
    try {
      if (Yv(
        t,
        s,
        e,
        n,
        dt
      )) {
        Nt = 1, rs(
          t,
          Ve(n, t.current)
        ), ft = null;
        return;
      }
    } catch (r) {
      if (s !== null) throw ft = s, r;
      Nt = 1, rs(
        t,
        Ve(n, t.current)
      ), ft = null;
      return;
    }
    e.flags & 32768 ? (gt || a === 1 ? t = !0 : ki || (dt & 536870912) !== 0 ? t = !1 : (Un = t = !0, (a === 2 || a === 9 || a === 3 || a === 6) && (a = Ae.current, a !== null && a.tag === 13 && (a.flags |= 16384))), fm(e, t)) : As(e);
  }
  function As(t) {
    var e = t;
    do {
      if ((e.flags & 32768) !== 0) {
        fm(
          e,
          Un
        );
        return;
      }
      t = e.return;
      var n = Xv(
        e.alternate,
        e,
        pn
      );
      if (n !== null) {
        ft = n;
        return;
      }
      if (e = e.sibling, e !== null) {
        ft = e;
        return;
      }
      ft = e = t;
    } while (e !== null);
    Nt === 0 && (Nt = 5);
  }
  function fm(t, e) {
    do {
      var n = Zv(t.alternate, t);
      if (n !== null) {
        n.flags &= 32767, ft = n;
        return;
      }
      if (n = t.return, n !== null && (n.flags |= 32768, n.subtreeFlags = 0, n.deletions = null), !e && (t = t.sibling, t !== null)) {
        ft = t;
        return;
      }
      ft = t = n;
    } while (t !== null);
    Nt = 6, ft = null;
  }
  function hm(t, e, n, a, s, r, f, p, T) {
    t.cancelPendingCommit = null;
    do
      Es();
    while (Jt !== 0);
    if ((bt & 6) !== 0) throw Error(o(327));
    if (e !== null) {
      if (e === t.current) throw Error(o(177));
      if (r = e.lanes | e.childLanes, r |= $u, V0(
        t,
        n,
        r,
        f,
        p,
        T
      ), t === zt && (ft = zt = null, dt = 0), Wi = e, jn = t, gn = n, ur = r, or = s, em = a, (e.subtreeFlags & 10256) !== 0 || (e.flags & 10256) !== 0 ? (t.callbackNode = null, t.callbackPriority = 0, n1(Ml, function() {
        return gm(), null;
      })) : (t.callbackNode = null, t.callbackPriority = 0), a = (e.flags & 13878) !== 0, (e.subtreeFlags & 13878) !== 0 || a) {
        a = O.T, O.T = null, s = X.p, X.p = 2, f = bt, bt |= 4;
        try {
          Qv(t, e, n);
        } finally {
          bt = f, X.p = s, O.T = a;
        }
      }
      Jt = 1, dm(), mm(), ym();
    }
  }
  function dm() {
    if (Jt === 1) {
      Jt = 0;
      var t = jn, e = Wi, n = (e.flags & 13878) !== 0;
      if ((e.subtreeFlags & 13878) !== 0 || n) {
        n = O.T, O.T = null;
        var a = X.p;
        X.p = 2;
        var s = bt;
        bt |= 4;
        try {
          Jd(e, t);
          var r = Er, f = If(t.containerInfo), p = r.focusedElem, T = r.selectionRange;
          if (f !== p && p && p.ownerDocument && $f(
            p.ownerDocument.documentElement,
            p
          )) {
            if (T !== null && Ju(p)) {
              var D = T.start, V = T.end;
              if (V === void 0 && (V = D), "selectionStart" in p)
                p.selectionStart = D, p.selectionEnd = Math.min(
                  V,
                  p.value.length
                );
              else {
                var B = p.ownerDocument || document, C = B && B.defaultView || window;
                if (C.getSelection) {
                  var R = C.getSelection(), k = p.textContent.length, et = Math.min(T.start, k), Ct = T.end === void 0 ? et : Math.min(T.end, k);
                  !R.extend && et > Ct && (f = Ct, Ct = et, et = f);
                  var x = Pf(
                    p,
                    et
                  ), A = Pf(
                    p,
                    Ct
                  );
                  if (x && A && (R.rangeCount !== 1 || R.anchorNode !== x.node || R.anchorOffset !== x.offset || R.focusNode !== A.node || R.focusOffset !== A.offset)) {
                    var M = B.createRange();
                    M.setStart(x.node, x.offset), R.removeAllRanges(), et > Ct ? (R.addRange(M), R.extend(A.node, A.offset)) : (M.setEnd(A.node, A.offset), R.addRange(M));
                  }
                }
              }
            }
            for (B = [], R = p; R = R.parentNode; )
              R.nodeType === 1 && B.push({
                element: R,
                left: R.scrollLeft,
                top: R.scrollTop
              });
            for (typeof p.focus == "function" && p.focus(), p = 0; p < B.length; p++) {
              var U = B[p];
              U.element.scrollLeft = U.left, U.element.scrollTop = U.top;
            }
          }
          Ns = !!Ar, Er = Ar = null;
        } finally {
          bt = s, X.p = a, O.T = n;
        }
      }
      t.current = e, Jt = 2;
    }
  }
  function mm() {
    if (Jt === 2) {
      Jt = 0;
      var t = jn, e = Wi, n = (e.flags & 8772) !== 0;
      if ((e.subtreeFlags & 8772) !== 0 || n) {
        n = O.T, O.T = null;
        var a = X.p;
        X.p = 2;
        var s = bt;
        bt |= 4;
        try {
          Gd(t, e.alternate, e);
        } finally {
          bt = s, X.p = a, O.T = n;
        }
      }
      Jt = 3;
    }
  }
  function ym() {
    if (Jt === 4 || Jt === 3) {
      Jt = 0, A0();
      var t = jn, e = Wi, n = gn, a = em;
      (e.subtreeFlags & 10256) !== 0 || (e.flags & 10256) !== 0 ? Jt = 5 : (Jt = 0, Wi = jn = null, pm(t, t.pendingLanes));
      var s = t.pendingLanes;
      if (s === 0 && (Nn = null), zu(n), e = e.stateNode, ve && typeof ve.onCommitFiberRoot == "function")
        try {
          ve.onCommitFiberRoot(
            ma,
            e,
            void 0,
            (e.current.flags & 128) === 128
          );
        } catch {
        }
      if (a !== null) {
        e = O.T, s = X.p, X.p = 2, O.T = null;
        try {
          for (var r = t.onRecoverableError, f = 0; f < a.length; f++) {
            var p = a[f];
            r(p.value, {
              componentStack: p.stack
            });
          }
        } finally {
          O.T = e, X.p = s;
        }
      }
      (gn & 3) !== 0 && Es(), Fe(t), s = t.pendingLanes, (n & 261930) !== 0 && (s & 42) !== 0 ? t === rr ? Fa++ : (Fa = 0, rr = t) : Fa = 0, Wa(0);
    }
  }
  function pm(t, e) {
    (t.pooledCacheLanes &= e) === 0 && (e = t.pooledCache, e != null && (t.pooledCache = null, Oa(e)));
  }
  function Es() {
    return dm(), mm(), ym(), gm();
  }
  function gm() {
    if (Jt !== 5) return !1;
    var t = jn, e = ur;
    ur = 0;
    var n = zu(gn), a = O.T, s = X.p;
    try {
      X.p = 32 > n ? 32 : n, O.T = null, n = or, or = null;
      var r = jn, f = gn;
      if (Jt = 0, Wi = jn = null, gn = 0, (bt & 6) !== 0) throw Error(o(331));
      var p = bt;
      if (bt |= 4, $d(r.current), Fd(
        r,
        r.current,
        f,
        n
      ), bt = p, Wa(0, !1), ve && typeof ve.onPostCommitFiberRoot == "function")
        try {
          ve.onPostCommitFiberRoot(ma, r);
        } catch {
        }
      return !0;
    } finally {
      X.p = s, O.T = a, pm(t, e);
    }
  }
  function vm(t, e, n) {
    e = Ve(n, e), e = qo(t.stateNode, e, 2), t = Rn(t, e, 2), t !== null && (pa(t, 2), Fe(t));
  }
  function xt(t, e, n) {
    if (t.tag === 3)
      vm(t, t, n);
    else
      for (; e !== null; ) {
        if (e.tag === 3) {
          vm(
            e,
            t,
            n
          );
          break;
        } else if (e.tag === 1) {
          var a = e.stateNode;
          if (typeof e.type.getDerivedStateFromError == "function" || typeof a.componentDidCatch == "function" && (Nn === null || !Nn.has(a))) {
            t = Ve(n, t), n = Sd(2), a = Rn(e, n, 2), a !== null && (Td(
              n,
              a,
              e,
              t
            ), pa(a, 2), Fe(a));
            break;
          }
        }
        e = e.return;
      }
  }
  function hr(t, e, n) {
    var a = t.pingCache;
    if (a === null) {
      a = t.pingCache = new kv();
      var s = /* @__PURE__ */ new Set();
      a.set(e, s);
    } else
      s = a.get(e), s === void 0 && (s = /* @__PURE__ */ new Set(), a.set(e, s));
    s.has(n) || (ar = !0, s.add(n), t = Iv.bind(null, t, e, n), e.then(t, t));
  }
  function Iv(t, e, n) {
    var a = t.pingCache;
    a !== null && a.delete(e), t.pingedLanes |= t.suspendedLanes & n, t.warmLanes &= ~n, zt === t && (dt & n) === n && (Nt === 4 || Nt === 3 && (dt & 62914560) === dt && 300 > ge() - gs ? (bt & 2) === 0 && Pi(t, 0) : lr |= n, Fi === dt && (Fi = 0)), Fe(t);
  }
  function Sm(t, e) {
    e === 0 && (e = df()), t = ei(t, e), t !== null && (pa(t, e), Fe(t));
  }
  function t1(t) {
    var e = t.memoizedState, n = 0;
    e !== null && (n = e.retryLane), Sm(t, n);
  }
  function e1(t, e) {
    var n = 0;
    switch (t.tag) {
      case 31:
      case 13:
        var a = t.stateNode, s = t.memoizedState;
        s !== null && (n = s.retryLane);
        break;
      case 19:
        a = t.stateNode;
        break;
      case 22:
        a = t.stateNode._retryCache;
        break;
      default:
        throw Error(o(314));
    }
    a !== null && a.delete(e), Sm(t, n);
  }
  function n1(t, e) {
    return xu(t, e);
  }
  var xs = null, Ii = null, dr = !1, Ms = !1, mr = !1, Ln = 0;
  function Fe(t) {
    t !== Ii && t.next === null && (Ii === null ? xs = Ii = t : Ii = Ii.next = t), Ms = !0, dr || (dr = !0, a1());
  }
  function Wa(t, e) {
    if (!mr && Ms) {
      mr = !0;
      do
        for (var n = !1, a = xs; a !== null; ) {
          if (t !== 0) {
            var s = a.pendingLanes;
            if (s === 0) var r = 0;
            else {
              var f = a.suspendedLanes, p = a.pingedLanes;
              r = (1 << 31 - Se(42 | t) + 1) - 1, r &= s & ~(f & ~p), r = r & 201326741 ? r & 201326741 | 1 : r ? r | 2 : 0;
            }
            r !== 0 && (n = !0, Em(a, r));
          } else
            r = dt, r = Rl(
              a,
              a === zt ? r : 0,
              a.cancelPendingCommit !== null || a.timeoutHandle !== -1
            ), (r & 3) === 0 || ya(a, r) || (n = !0, Em(a, r));
          a = a.next;
        }
      while (n);
      mr = !1;
    }
  }
  function i1() {
    Tm();
  }
  function Tm() {
    Ms = dr = !1;
    var t = 0;
    Ln !== 0 && m1() && (t = Ln);
    for (var e = ge(), n = null, a = xs; a !== null; ) {
      var s = a.next, r = bm(a, e);
      r === 0 ? (a.next = null, n === null ? xs = s : n.next = s, s === null && (Ii = n)) : (n = a, (t !== 0 || (r & 3) !== 0) && (Ms = !0)), a = s;
    }
    Jt !== 0 && Jt !== 5 || Wa(t), Ln !== 0 && (Ln = 0);
  }
  function bm(t, e) {
    for (var n = t.suspendedLanes, a = t.pingedLanes, s = t.expirationTimes, r = t.pendingLanes & -62914561; 0 < r; ) {
      var f = 31 - Se(r), p = 1 << f, T = s[f];
      T === -1 ? ((p & n) === 0 || (p & a) !== 0) && (s[f] = O0(p, e)) : T <= e && (t.expiredLanes |= p), r &= ~p;
    }
    if (e = zt, n = dt, n = Rl(
      t,
      t === e ? n : 0,
      t.cancelPendingCommit !== null || t.timeoutHandle !== -1
    ), a = t.callbackNode, n === 0 || t === e && (Et === 2 || Et === 9) || t.cancelPendingCommit !== null)
      return a !== null && a !== null && Mu(a), t.callbackNode = null, t.callbackPriority = 0;
    if ((n & 3) === 0 || ya(t, n)) {
      if (e = n & -n, e === t.callbackPriority) return e;
      switch (a !== null && Mu(a), zu(n)) {
        case 2:
        case 8:
          n = ff;
          break;
        case 32:
          n = Ml;
          break;
        case 268435456:
          n = hf;
          break;
        default:
          n = Ml;
      }
      return a = Am.bind(null, t), n = xu(n, a), t.callbackPriority = e, t.callbackNode = n, e;
    }
    return a !== null && a !== null && Mu(a), t.callbackPriority = 2, t.callbackNode = null, 2;
  }
  function Am(t, e) {
    if (Jt !== 0 && Jt !== 5)
      return t.callbackNode = null, t.callbackPriority = 0, null;
    var n = t.callbackNode;
    if (Es() && t.callbackNode !== n)
      return null;
    var a = dt;
    return a = Rl(
      t,
      t === zt ? a : 0,
      t.cancelPendingCommit !== null || t.timeoutHandle !== -1
    ), a === 0 ? null : (im(t, a, e), bm(t, ge()), t.callbackNode != null && t.callbackNode === n ? Am.bind(null, t) : null);
  }
  function Em(t, e) {
    if (Es()) return null;
    im(t, e, !0);
  }
  function a1() {
    p1(function() {
      (bt & 6) !== 0 ? xu(
        cf,
        i1
      ) : Tm();
    });
  }
  function yr() {
    if (Ln === 0) {
      var t = Li;
      t === 0 && (t = Dl, Dl <<= 1, (Dl & 261888) === 0 && (Dl = 256)), Ln = t;
    }
    return Ln;
  }
  function xm(t) {
    return t == null || typeof t == "symbol" || typeof t == "boolean" ? null : typeof t == "function" ? t : Ul("" + t);
  }
  function Mm(t, e) {
    var n = e.ownerDocument.createElement("input");
    return n.name = e.name, n.value = e.value, t.id && n.setAttribute("form", t.id), e.parentNode.insertBefore(n, e), t = new FormData(t), n.parentNode.removeChild(n), t;
  }
  function l1(t, e, n, a, s) {
    if (e === "submit" && n && n.stateNode === s) {
      var r = xm(
        (s[ce] || null).action
      ), f = a.submitter;
      f && (e = (e = f[ce] || null) ? xm(e.formAction) : f.getAttribute("formAction"), e !== null && (r = e, f = null));
      var p = new wl(
        "action",
        "action",
        null,
        a,
        s
      );
      t.push({
        event: p,
        listeners: [
          {
            instance: null,
            listener: function() {
              if (a.defaultPrevented) {
                if (Ln !== 0) {
                  var T = f ? Mm(s, f) : new FormData(s);
                  No(
                    n,
                    {
                      pending: !0,
                      data: T,
                      method: s.method,
                      action: r
                    },
                    null,
                    T
                  );
                }
              } else
                typeof r == "function" && (p.preventDefault(), T = f ? Mm(s, f) : new FormData(s), No(
                  n,
                  {
                    pending: !0,
                    data: T,
                    method: s.method,
                    action: r
                  },
                  r,
                  T
                ));
            },
            currentTarget: s
          }
        ]
      });
    }
  }
  for (var pr = 0; pr < Pu.length; pr++) {
    var gr = Pu[pr], s1 = gr.toLowerCase(), u1 = gr[0].toUpperCase() + gr.slice(1);
    Ye(
      s1,
      "on" + u1
    );
  }
  Ye(nh, "onAnimationEnd"), Ye(ih, "onAnimationIteration"), Ye(ah, "onAnimationStart"), Ye("dblclick", "onDoubleClick"), Ye("focusin", "onFocus"), Ye("focusout", "onBlur"), Ye(Ev, "onTransitionRun"), Ye(xv, "onTransitionStart"), Ye(Mv, "onTransitionCancel"), Ye(lh, "onTransitionEnd"), xi("onMouseEnter", ["mouseout", "mouseover"]), xi("onMouseLeave", ["mouseout", "mouseover"]), xi("onPointerEnter", ["pointerout", "pointerover"]), xi("onPointerLeave", ["pointerout", "pointerover"]), Pn(
    "onChange",
    "change click focusin focusout input keydown keyup selectionchange".split(" ")
  ), Pn(
    "onSelect",
    "focusout contextmenu dragend focusin keydown keyup mousedown mouseup selectionchange".split(
      " "
    )
  ), Pn("onBeforeInput", [
    "compositionend",
    "keypress",
    "textInput",
    "paste"
  ]), Pn(
    "onCompositionEnd",
    "compositionend focusout keydown keypress keyup mousedown".split(" ")
  ), Pn(
    "onCompositionStart",
    "compositionstart focusout keydown keypress keyup mousedown".split(" ")
  ), Pn(
    "onCompositionUpdate",
    "compositionupdate focusout keydown keypress keyup mousedown".split(" ")
  );
  var Pa = "abort canplay canplaythrough durationchange emptied encrypted ended error loadeddata loadedmetadata loadstart pause play playing progress ratechange resize seeked seeking stalled suspend timeupdate volumechange waiting".split(
    " "
  ), o1 = new Set(
    "beforetoggle cancel close invalid load scroll scrollend toggle".split(" ").concat(Pa)
  );
  function Dm(t, e) {
    e = (e & 4) !== 0;
    for (var n = 0; n < t.length; n++) {
      var a = t[n], s = a.event;
      a = a.listeners;
      t: {
        var r = void 0;
        if (e)
          for (var f = a.length - 1; 0 <= f; f--) {
            var p = a[f], T = p.instance, D = p.currentTarget;
            if (p = p.listener, T !== r && s.isPropagationStopped())
              break t;
            r = p, s.currentTarget = D;
            try {
              r(s);
            } catch (V) {
              Yl(V);
            }
            s.currentTarget = null, r = T;
          }
        else
          for (f = 0; f < a.length; f++) {
            if (p = a[f], T = p.instance, D = p.currentTarget, p = p.listener, T !== r && s.isPropagationStopped())
              break t;
            r = p, s.currentTarget = D;
            try {
              r(s);
            } catch (V) {
              Yl(V);
            }
            s.currentTarget = null, r = T;
          }
      }
    }
  }
  function ht(t, e) {
    var n = e[Ru];
    n === void 0 && (n = e[Ru] = /* @__PURE__ */ new Set());
    var a = t + "__bubble";
    n.has(a) || (Cm(e, t, 2, !1), n.add(a));
  }
  function vr(t, e, n) {
    var a = 0;
    e && (a |= 4), Cm(
      n,
      t,
      a,
      e
    );
  }
  var Ds = "_reactListening" + Math.random().toString(36).slice(2);
  function Sr(t) {
    if (!t[Ds]) {
      t[Ds] = !0, Tf.forEach(function(n) {
        n !== "selectionchange" && (o1.has(n) || vr(n, !1, t), vr(n, !0, t));
      });
      var e = t.nodeType === 9 ? t : t.ownerDocument;
      e === null || e[Ds] || (e[Ds] = !0, vr("selectionchange", !1, e));
    }
  }
  function Cm(t, e, n, a) {
    switch (ny(e)) {
      case 2:
        var s = j1;
        break;
      case 8:
        s = w1;
        break;
      default:
        s = Br;
    }
    n = s.bind(
      null,
      e,
      n,
      t
    ), s = void 0, !Lu || e !== "touchstart" && e !== "touchmove" && e !== "wheel" || (s = !0), a ? s !== void 0 ? t.addEventListener(e, n, {
      capture: !0,
      passive: s
    }) : t.addEventListener(e, n, !0) : s !== void 0 ? t.addEventListener(e, n, {
      passive: s
    }) : t.addEventListener(e, n, !1);
  }
  function Tr(t, e, n, a, s) {
    var r = a;
    if ((e & 1) === 0 && (e & 2) === 0 && a !== null)
      t: for (; ; ) {
        if (a === null) return;
        var f = a.tag;
        if (f === 3 || f === 4) {
          var p = a.stateNode.containerInfo;
          if (p === s) break;
          if (f === 4)
            for (f = a.return; f !== null; ) {
              var T = f.tag;
              if ((T === 3 || T === 4) && f.stateNode.containerInfo === s)
                return;
              f = f.return;
            }
          for (; p !== null; ) {
            if (f = bi(p), f === null) return;
            if (T = f.tag, T === 5 || T === 6 || T === 26 || T === 27) {
              a = r = f;
              continue t;
            }
            p = p.parentNode;
          }
        }
        a = a.return;
      }
    _f(function() {
      var D = r, V = ju(n), B = [];
      t: {
        var C = sh.get(t);
        if (C !== void 0) {
          var R = wl, k = t;
          switch (t) {
            case "keypress":
              if (Nl(n) === 0) break t;
            case "keydown":
            case "keyup":
              R = ev;
              break;
            case "focusin":
              k = "focus", R = Gu;
              break;
            case "focusout":
              k = "blur", R = Gu;
              break;
            case "beforeblur":
            case "afterblur":
              R = Gu;
              break;
            case "click":
              if (n.button === 2) break t;
            case "auxclick":
            case "dblclick":
            case "mousedown":
            case "mousemove":
            case "mouseup":
            case "mouseout":
            case "mouseover":
            case "contextmenu":
              R = Nf;
              break;
            case "drag":
            case "dragend":
            case "dragenter":
            case "dragexit":
            case "dragleave":
            case "dragover":
            case "dragstart":
            case "drop":
              R = X0;
              break;
            case "touchcancel":
            case "touchend":
            case "touchmove":
            case "touchstart":
              R = av;
              break;
            case nh:
            case ih:
            case ah:
              R = K0;
              break;
            case lh:
              R = sv;
              break;
            case "scroll":
            case "scrollend":
              R = q0;
              break;
            case "wheel":
              R = ov;
              break;
            case "copy":
            case "cut":
            case "paste":
              R = k0;
              break;
            case "gotpointercapture":
            case "lostpointercapture":
            case "pointercancel":
            case "pointerdown":
            case "pointermove":
            case "pointerout":
            case "pointerover":
            case "pointerup":
              R = wf;
              break;
            case "toggle":
            case "beforetoggle":
              R = cv;
          }
          var et = (e & 4) !== 0, Ct = !et && (t === "scroll" || t === "scrollend"), x = et ? C !== null ? C + "Capture" : null : C;
          et = [];
          for (var A = D, M; A !== null; ) {
            var U = A;
            if (M = U.stateNode, U = U.tag, U !== 5 && U !== 26 && U !== 27 || M === null || x === null || (U = Sa(A, x), U != null && et.push(
              $a(A, U, M)
            )), Ct) break;
            A = A.return;
          }
          0 < et.length && (C = new R(
            C,
            k,
            null,
            n,
            V
          ), B.push({ event: C, listeners: et }));
        }
      }
      if ((e & 7) === 0) {
        t: {
          if (C = t === "mouseover" || t === "pointerover", R = t === "mouseout" || t === "pointerout", C && n !== Nu && (k = n.relatedTarget || n.fromElement) && (bi(k) || k[Ti]))
            break t;
          if ((R || C) && (C = V.window === V ? V : (C = V.ownerDocument) ? C.defaultView || C.parentWindow : window, R ? (k = n.relatedTarget || n.toElement, R = D, k = k ? bi(k) : null, k !== null && (Ct = d(k), et = k.tag, k !== Ct || et !== 5 && et !== 27 && et !== 6) && (k = null)) : (R = null, k = D), R !== k)) {
            if (et = Nf, U = "onMouseLeave", x = "onMouseEnter", A = "mouse", (t === "pointerout" || t === "pointerover") && (et = wf, U = "onPointerLeave", x = "onPointerEnter", A = "pointer"), Ct = R == null ? C : va(R), M = k == null ? C : va(k), C = new et(
              U,
              A + "leave",
              R,
              n,
              V
            ), C.target = Ct, C.relatedTarget = M, U = null, bi(V) === D && (et = new et(
              x,
              A + "enter",
              k,
              n,
              V
            ), et.target = M, et.relatedTarget = Ct, U = et), Ct = U, R && k)
              e: {
                for (et = r1, x = R, A = k, M = 0, U = x; U; U = et(U))
                  M++;
                U = 0;
                for (var I = A; I; I = et(I))
                  U++;
                for (; 0 < M - U; )
                  x = et(x), M--;
                for (; 0 < U - M; )
                  A = et(A), U--;
                for (; M--; ) {
                  if (x === A || A !== null && x === A.alternate) {
                    et = x;
                    break e;
                  }
                  x = et(x), A = et(A);
                }
                et = null;
              }
            else et = null;
            R !== null && zm(
              B,
              C,
              R,
              et,
              !1
            ), k !== null && Ct !== null && zm(
              B,
              Ct,
              k,
              et,
              !0
            );
          }
        }
        t: {
          if (C = D ? va(D) : window, R = C.nodeName && C.nodeName.toLowerCase(), R === "select" || R === "input" && C.type === "file")
            var St = Qf;
          else if (Xf(C))
            if (Kf)
              St = Tv;
            else {
              St = vv;
              var P = gv;
            }
          else
            R = C.nodeName, !R || R.toLowerCase() !== "input" || C.type !== "checkbox" && C.type !== "radio" ? D && Bu(D.elementType) && (St = Qf) : St = Sv;
          if (St && (St = St(t, D))) {
            Zf(
              B,
              St,
              n,
              V
            );
            break t;
          }
          P && P(t, C, D), t === "focusout" && D && C.type === "number" && D.memoizedProps.value != null && Uu(C, "number", C.value);
        }
        switch (P = D ? va(D) : window, t) {
          case "focusin":
            (Xf(P) || P.contentEditable === "true") && (Oi = P, ku = D, Ca = null);
            break;
          case "focusout":
            Ca = ku = Oi = null;
            break;
          case "mousedown":
            Fu = !0;
            break;
          case "contextmenu":
          case "mouseup":
          case "dragend":
            Fu = !1, th(B, n, V);
            break;
          case "selectionchange":
            if (Av) break;
          case "keydown":
          case "keyup":
            th(B, n, V);
        }
        var ot;
        if (Zu)
          t: {
            switch (t) {
              case "compositionstart":
                var mt = "onCompositionStart";
                break t;
              case "compositionend":
                mt = "onCompositionEnd";
                break t;
              case "compositionupdate":
                mt = "onCompositionUpdate";
                break t;
            }
            mt = void 0;
          }
        else
          Ri ? qf(t, n) && (mt = "onCompositionEnd") : t === "keydown" && n.keyCode === 229 && (mt = "onCompositionStart");
        mt && (Lf && n.locale !== "ko" && (Ri || mt !== "onCompositionStart" ? mt === "onCompositionEnd" && Ri && (ot = Uf()) : (An = V, Hu = "value" in An ? An.value : An.textContent, Ri = !0)), P = Cs(D, mt), 0 < P.length && (mt = new jf(
          mt,
          t,
          null,
          n,
          V
        ), B.push({ event: mt, listeners: P }), ot ? mt.data = ot : (ot = Gf(n), ot !== null && (mt.data = ot)))), (ot = hv ? dv(t, n) : mv(t, n)) && (mt = Cs(D, "onBeforeInput"), 0 < mt.length && (P = new jf(
          "onBeforeInput",
          "beforeinput",
          null,
          n,
          V
        ), B.push({
          event: P,
          listeners: mt
        }), P.data = ot)), l1(
          B,
          t,
          D,
          n,
          V
        );
      }
      Dm(B, e);
    });
  }
  function $a(t, e, n) {
    return {
      instance: t,
      listener: e,
      currentTarget: n
    };
  }
  function Cs(t, e) {
    for (var n = e + "Capture", a = []; t !== null; ) {
      var s = t, r = s.stateNode;
      if (s = s.tag, s !== 5 && s !== 26 && s !== 27 || r === null || (s = Sa(t, n), s != null && a.unshift(
        $a(t, s, r)
      ), s = Sa(t, e), s != null && a.push(
        $a(t, s, r)
      )), t.tag === 3) return a;
      t = t.return;
    }
    return [];
  }
  function r1(t) {
    if (t === null) return null;
    do
      t = t.return;
    while (t && t.tag !== 5 && t.tag !== 27);
    return t || null;
  }
  function zm(t, e, n, a, s) {
    for (var r = e._reactName, f = []; n !== null && n !== a; ) {
      var p = n, T = p.alternate, D = p.stateNode;
      if (p = p.tag, T !== null && T === a) break;
      p !== 5 && p !== 26 && p !== 27 || D === null || (T = D, s ? (D = Sa(n, r), D != null && f.unshift(
        $a(n, D, T)
      )) : s || (D = Sa(n, r), D != null && f.push(
        $a(n, D, T)
      ))), n = n.return;
    }
    f.length !== 0 && t.push({ event: e, listeners: f });
  }
  var c1 = /\r\n?/g, f1 = /\u0000|\uFFFD/g;
  function Rm(t) {
    return (typeof t == "string" ? t : "" + t).replace(c1, `
`).replace(f1, "");
  }
  function Om(t, e) {
    return e = Rm(e), Rm(t) === e;
  }
  function Dt(t, e, n, a, s, r) {
    switch (n) {
      case "children":
        typeof a == "string" ? e === "body" || e === "textarea" && a === "" || Di(t, a) : (typeof a == "number" || typeof a == "bigint") && e !== "body" && Di(t, "" + a);
        break;
      case "className":
        Vl(t, "class", a);
        break;
      case "tabIndex":
        Vl(t, "tabindex", a);
        break;
      case "dir":
      case "role":
      case "viewBox":
      case "width":
      case "height":
        Vl(t, n, a);
        break;
      case "style":
        Of(t, a, r);
        break;
      case "data":
        if (e !== "object") {
          Vl(t, "data", a);
          break;
        }
      case "src":
      case "href":
        if (a === "" && (e !== "a" || n !== "href")) {
          t.removeAttribute(n);
          break;
        }
        if (a == null || typeof a == "function" || typeof a == "symbol" || typeof a == "boolean") {
          t.removeAttribute(n);
          break;
        }
        a = Ul("" + a), t.setAttribute(n, a);
        break;
      case "action":
      case "formAction":
        if (typeof a == "function") {
          t.setAttribute(
            n,
            "javascript:throw new Error('A React form was unexpectedly submitted. If you called form.submit() manually, consider using form.requestSubmit() instead. If you\\'re trying to use event.stopPropagation() in a submit event handler, consider also calling event.preventDefault().')"
          );
          break;
        } else
          typeof r == "function" && (n === "formAction" ? (e !== "input" && Dt(t, e, "name", s.name, s, null), Dt(
            t,
            e,
            "formEncType",
            s.formEncType,
            s,
            null
          ), Dt(
            t,
            e,
            "formMethod",
            s.formMethod,
            s,
            null
          ), Dt(
            t,
            e,
            "formTarget",
            s.formTarget,
            s,
            null
          )) : (Dt(t, e, "encType", s.encType, s, null), Dt(t, e, "method", s.method, s, null), Dt(t, e, "target", s.target, s, null)));
        if (a == null || typeof a == "symbol" || typeof a == "boolean") {
          t.removeAttribute(n);
          break;
        }
        a = Ul("" + a), t.setAttribute(n, a);
        break;
      case "onClick":
        a != null && (t.onclick = en);
        break;
      case "onScroll":
        a != null && ht("scroll", t);
        break;
      case "onScrollEnd":
        a != null && ht("scrollend", t);
        break;
      case "dangerouslySetInnerHTML":
        if (a != null) {
          if (typeof a != "object" || !("__html" in a))
            throw Error(o(61));
          if (n = a.__html, n != null) {
            if (s.children != null) throw Error(o(60));
            t.innerHTML = n;
          }
        }
        break;
      case "multiple":
        t.multiple = a && typeof a != "function" && typeof a != "symbol";
        break;
      case "muted":
        t.muted = a && typeof a != "function" && typeof a != "symbol";
        break;
      case "suppressContentEditableWarning":
      case "suppressHydrationWarning":
      case "defaultValue":
      case "defaultChecked":
      case "innerHTML":
      case "ref":
        break;
      case "autoFocus":
        break;
      case "xlinkHref":
        if (a == null || typeof a == "function" || typeof a == "boolean" || typeof a == "symbol") {
          t.removeAttribute("xlink:href");
          break;
        }
        n = Ul("" + a), t.setAttributeNS(
          "http://www.w3.org/1999/xlink",
          "xlink:href",
          n
        );
        break;
      case "contentEditable":
      case "spellCheck":
      case "draggable":
      case "value":
      case "autoReverse":
      case "externalResourcesRequired":
      case "focusable":
      case "preserveAlpha":
        a != null && typeof a != "function" && typeof a != "symbol" ? t.setAttribute(n, "" + a) : t.removeAttribute(n);
        break;
      case "inert":
      case "allowFullScreen":
      case "async":
      case "autoPlay":
      case "controls":
      case "default":
      case "defer":
      case "disabled":
      case "disablePictureInPicture":
      case "disableRemotePlayback":
      case "formNoValidate":
      case "hidden":
      case "loop":
      case "noModule":
      case "noValidate":
      case "open":
      case "playsInline":
      case "readOnly":
      case "required":
      case "reversed":
      case "scoped":
      case "seamless":
      case "itemScope":
        a && typeof a != "function" && typeof a != "symbol" ? t.setAttribute(n, "") : t.removeAttribute(n);
        break;
      case "capture":
      case "download":
        a === !0 ? t.setAttribute(n, "") : a !== !1 && a != null && typeof a != "function" && typeof a != "symbol" ? t.setAttribute(n, a) : t.removeAttribute(n);
        break;
      case "cols":
      case "rows":
      case "size":
      case "span":
        a != null && typeof a != "function" && typeof a != "symbol" && !isNaN(a) && 1 <= a ? t.setAttribute(n, a) : t.removeAttribute(n);
        break;
      case "rowSpan":
      case "start":
        a == null || typeof a == "function" || typeof a == "symbol" || isNaN(a) ? t.removeAttribute(n) : t.setAttribute(n, a);
        break;
      case "popover":
        ht("beforetoggle", t), ht("toggle", t), Ol(t, "popover", a);
        break;
      case "xlinkActuate":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:actuate",
          a
        );
        break;
      case "xlinkArcrole":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:arcrole",
          a
        );
        break;
      case "xlinkRole":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:role",
          a
        );
        break;
      case "xlinkShow":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:show",
          a
        );
        break;
      case "xlinkTitle":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:title",
          a
        );
        break;
      case "xlinkType":
        tn(
          t,
          "http://www.w3.org/1999/xlink",
          "xlink:type",
          a
        );
        break;
      case "xmlBase":
        tn(
          t,
          "http://www.w3.org/XML/1998/namespace",
          "xml:base",
          a
        );
        break;
      case "xmlLang":
        tn(
          t,
          "http://www.w3.org/XML/1998/namespace",
          "xml:lang",
          a
        );
        break;
      case "xmlSpace":
        tn(
          t,
          "http://www.w3.org/XML/1998/namespace",
          "xml:space",
          a
        );
        break;
      case "is":
        Ol(t, "is", a);
        break;
      case "innerText":
      case "textContent":
        break;
      default:
        (!(2 < n.length) || n[0] !== "o" && n[0] !== "O" || n[1] !== "n" && n[1] !== "N") && (n = H0.get(n) || n, Ol(t, n, a));
    }
  }
  function br(t, e, n, a, s, r) {
    switch (n) {
      case "style":
        Of(t, a, r);
        break;
      case "dangerouslySetInnerHTML":
        if (a != null) {
          if (typeof a != "object" || !("__html" in a))
            throw Error(o(61));
          if (n = a.__html, n != null) {
            if (s.children != null) throw Error(o(60));
            t.innerHTML = n;
          }
        }
        break;
      case "children":
        typeof a == "string" ? Di(t, a) : (typeof a == "number" || typeof a == "bigint") && Di(t, "" + a);
        break;
      case "onScroll":
        a != null && ht("scroll", t);
        break;
      case "onScrollEnd":
        a != null && ht("scrollend", t);
        break;
      case "onClick":
        a != null && (t.onclick = en);
        break;
      case "suppressContentEditableWarning":
      case "suppressHydrationWarning":
      case "innerHTML":
      case "ref":
        break;
      case "innerText":
      case "textContent":
        break;
      default:
        if (!bf.hasOwnProperty(n))
          t: {
            if (n[0] === "o" && n[1] === "n" && (s = n.endsWith("Capture"), e = n.slice(2, s ? n.length - 7 : void 0), r = t[ce] || null, r = r != null ? r[n] : null, typeof r == "function" && t.removeEventListener(e, r, s), typeof a == "function")) {
              typeof r != "function" && r !== null && (n in t ? t[n] = null : t.hasAttribute(n) && t.removeAttribute(n)), t.addEventListener(e, a, s);
              break t;
            }
            n in t ? t[n] = a : a === !0 ? t.setAttribute(n, "") : Ol(t, n, a);
          }
    }
  }
  function ne(t, e, n) {
    switch (e) {
      case "div":
      case "span":
      case "svg":
      case "path":
      case "a":
      case "g":
      case "p":
      case "li":
        break;
      case "img":
        ht("error", t), ht("load", t);
        var a = !1, s = !1, r;
        for (r in n)
          if (n.hasOwnProperty(r)) {
            var f = n[r];
            if (f != null)
              switch (r) {
                case "src":
                  a = !0;
                  break;
                case "srcSet":
                  s = !0;
                  break;
                case "children":
                case "dangerouslySetInnerHTML":
                  throw Error(o(137, e));
                default:
                  Dt(t, e, r, f, n, null);
              }
          }
        s && Dt(t, e, "srcSet", n.srcSet, n, null), a && Dt(t, e, "src", n.src, n, null);
        return;
      case "input":
        ht("invalid", t);
        var p = r = f = s = null, T = null, D = null;
        for (a in n)
          if (n.hasOwnProperty(a)) {
            var V = n[a];
            if (V != null)
              switch (a) {
                case "name":
                  s = V;
                  break;
                case "type":
                  f = V;
                  break;
                case "checked":
                  T = V;
                  break;
                case "defaultChecked":
                  D = V;
                  break;
                case "value":
                  r = V;
                  break;
                case "defaultValue":
                  p = V;
                  break;
                case "children":
                case "dangerouslySetInnerHTML":
                  if (V != null)
                    throw Error(o(137, e));
                  break;
                default:
                  Dt(t, e, a, V, n, null);
              }
          }
        Df(
          t,
          r,
          p,
          T,
          D,
          f,
          s,
          !1
        );
        return;
      case "select":
        ht("invalid", t), a = f = r = null;
        for (s in n)
          if (n.hasOwnProperty(s) && (p = n[s], p != null))
            switch (s) {
              case "value":
                r = p;
                break;
              case "defaultValue":
                f = p;
                break;
              case "multiple":
                a = p;
              default:
                Dt(t, e, s, p, n, null);
            }
        e = r, n = f, t.multiple = !!a, e != null ? Mi(t, !!a, e, !1) : n != null && Mi(t, !!a, n, !0);
        return;
      case "textarea":
        ht("invalid", t), r = s = a = null;
        for (f in n)
          if (n.hasOwnProperty(f) && (p = n[f], p != null))
            switch (f) {
              case "value":
                a = p;
                break;
              case "defaultValue":
                s = p;
                break;
              case "children":
                r = p;
                break;
              case "dangerouslySetInnerHTML":
                if (p != null) throw Error(o(91));
                break;
              default:
                Dt(t, e, f, p, n, null);
            }
        zf(t, a, s, r);
        return;
      case "option":
        for (T in n)
          n.hasOwnProperty(T) && (a = n[T], a != null) && (T === "selected" ? t.selected = a && typeof a != "function" && typeof a != "symbol" : Dt(t, e, T, a, n, null));
        return;
      case "dialog":
        ht("beforetoggle", t), ht("toggle", t), ht("cancel", t), ht("close", t);
        break;
      case "iframe":
      case "object":
        ht("load", t);
        break;
      case "video":
      case "audio":
        for (a = 0; a < Pa.length; a++)
          ht(Pa[a], t);
        break;
      case "image":
        ht("error", t), ht("load", t);
        break;
      case "details":
        ht("toggle", t);
        break;
      case "embed":
      case "source":
      case "link":
        ht("error", t), ht("load", t);
      case "area":
      case "base":
      case "br":
      case "col":
      case "hr":
      case "keygen":
      case "meta":
      case "param":
      case "track":
      case "wbr":
      case "menuitem":
        for (D in n)
          if (n.hasOwnProperty(D) && (a = n[D], a != null))
            switch (D) {
              case "children":
              case "dangerouslySetInnerHTML":
                throw Error(o(137, e));
              default:
                Dt(t, e, D, a, n, null);
            }
        return;
      default:
        if (Bu(e)) {
          for (V in n)
            n.hasOwnProperty(V) && (a = n[V], a !== void 0 && br(
              t,
              e,
              V,
              a,
              n,
              void 0
            ));
          return;
        }
    }
    for (p in n)
      n.hasOwnProperty(p) && (a = n[p], a != null && Dt(t, e, p, a, n, null));
  }
  function h1(t, e, n, a) {
    switch (e) {
      case "div":
      case "span":
      case "svg":
      case "path":
      case "a":
      case "g":
      case "p":
      case "li":
        break;
      case "input":
        var s = null, r = null, f = null, p = null, T = null, D = null, V = null;
        for (R in n) {
          var B = n[R];
          if (n.hasOwnProperty(R) && B != null)
            switch (R) {
              case "checked":
                break;
              case "value":
                break;
              case "defaultValue":
                T = B;
              default:
                a.hasOwnProperty(R) || Dt(t, e, R, null, a, B);
            }
        }
        for (var C in a) {
          var R = a[C];
          if (B = n[C], a.hasOwnProperty(C) && (R != null || B != null))
            switch (C) {
              case "type":
                r = R;
                break;
              case "name":
                s = R;
                break;
              case "checked":
                D = R;
                break;
              case "defaultChecked":
                V = R;
                break;
              case "value":
                f = R;
                break;
              case "defaultValue":
                p = R;
                break;
              case "children":
              case "dangerouslySetInnerHTML":
                if (R != null)
                  throw Error(o(137, e));
                break;
              default:
                R !== B && Dt(
                  t,
                  e,
                  C,
                  R,
                  a,
                  B
                );
            }
        }
        _u(
          t,
          f,
          p,
          T,
          D,
          V,
          r,
          s
        );
        return;
      case "select":
        R = f = p = C = null;
        for (r in n)
          if (T = n[r], n.hasOwnProperty(r) && T != null)
            switch (r) {
              case "value":
                break;
              case "multiple":
                R = T;
              default:
                a.hasOwnProperty(r) || Dt(
                  t,
                  e,
                  r,
                  null,
                  a,
                  T
                );
            }
        for (s in a)
          if (r = a[s], T = n[s], a.hasOwnProperty(s) && (r != null || T != null))
            switch (s) {
              case "value":
                C = r;
                break;
              case "defaultValue":
                p = r;
                break;
              case "multiple":
                f = r;
              default:
                r !== T && Dt(
                  t,
                  e,
                  s,
                  r,
                  a,
                  T
                );
            }
        e = p, n = f, a = R, C != null ? Mi(t, !!n, C, !1) : !!a != !!n && (e != null ? Mi(t, !!n, e, !0) : Mi(t, !!n, n ? [] : "", !1));
        return;
      case "textarea":
        R = C = null;
        for (p in n)
          if (s = n[p], n.hasOwnProperty(p) && s != null && !a.hasOwnProperty(p))
            switch (p) {
              case "value":
                break;
              case "children":
                break;
              default:
                Dt(t, e, p, null, a, s);
            }
        for (f in a)
          if (s = a[f], r = n[f], a.hasOwnProperty(f) && (s != null || r != null))
            switch (f) {
              case "value":
                C = s;
                break;
              case "defaultValue":
                R = s;
                break;
              case "children":
                break;
              case "dangerouslySetInnerHTML":
                if (s != null) throw Error(o(91));
                break;
              default:
                s !== r && Dt(t, e, f, s, a, r);
            }
        Cf(t, C, R);
        return;
      case "option":
        for (var k in n)
          C = n[k], n.hasOwnProperty(k) && C != null && !a.hasOwnProperty(k) && (k === "selected" ? t.selected = !1 : Dt(
            t,
            e,
            k,
            null,
            a,
            C
          ));
        for (T in a)
          C = a[T], R = n[T], a.hasOwnProperty(T) && C !== R && (C != null || R != null) && (T === "selected" ? t.selected = C && typeof C != "function" && typeof C != "symbol" : Dt(
            t,
            e,
            T,
            C,
            a,
            R
          ));
        return;
      case "img":
      case "link":
      case "area":
      case "base":
      case "br":
      case "col":
      case "embed":
      case "hr":
      case "keygen":
      case "meta":
      case "param":
      case "source":
      case "track":
      case "wbr":
      case "menuitem":
        for (var et in n)
          C = n[et], n.hasOwnProperty(et) && C != null && !a.hasOwnProperty(et) && Dt(t, e, et, null, a, C);
        for (D in a)
          if (C = a[D], R = n[D], a.hasOwnProperty(D) && C !== R && (C != null || R != null))
            switch (D) {
              case "children":
              case "dangerouslySetInnerHTML":
                if (C != null)
                  throw Error(o(137, e));
                break;
              default:
                Dt(
                  t,
                  e,
                  D,
                  C,
                  a,
                  R
                );
            }
        return;
      default:
        if (Bu(e)) {
          for (var Ct in n)
            C = n[Ct], n.hasOwnProperty(Ct) && C !== void 0 && !a.hasOwnProperty(Ct) && br(
              t,
              e,
              Ct,
              void 0,
              a,
              C
            );
          for (V in a)
            C = a[V], R = n[V], !a.hasOwnProperty(V) || C === R || C === void 0 && R === void 0 || br(
              t,
              e,
              V,
              C,
              a,
              R
            );
          return;
        }
    }
    for (var x in n)
      C = n[x], n.hasOwnProperty(x) && C != null && !a.hasOwnProperty(x) && Dt(t, e, x, null, a, C);
    for (B in a)
      C = a[B], R = n[B], !a.hasOwnProperty(B) || C === R || C == null && R == null || Dt(t, e, B, C, a, R);
  }
  function Vm(t) {
    switch (t) {
      case "css":
      case "script":
      case "font":
      case "img":
      case "image":
      case "input":
      case "link":
        return !0;
      default:
        return !1;
    }
  }
  function d1() {
    if (typeof performance.getEntriesByType == "function") {
      for (var t = 0, e = 0, n = performance.getEntriesByType("resource"), a = 0; a < n.length; a++) {
        var s = n[a], r = s.transferSize, f = s.initiatorType, p = s.duration;
        if (r && p && Vm(f)) {
          for (f = 0, p = s.responseEnd, a += 1; a < n.length; a++) {
            var T = n[a], D = T.startTime;
            if (D > p) break;
            var V = T.transferSize, B = T.initiatorType;
            V && Vm(B) && (T = T.responseEnd, f += V * (T < p ? 1 : (p - D) / (T - D)));
          }
          if (--a, e += 8 * (r + f) / (s.duration / 1e3), t++, 10 < t) break;
        }
      }
      if (0 < t) return e / t / 1e6;
    }
    return navigator.connection && (t = navigator.connection.downlink, typeof t == "number") ? t : 5;
  }
  var Ar = null, Er = null;
  function zs(t) {
    return t.nodeType === 9 ? t : t.ownerDocument;
  }
  function _m(t) {
    switch (t) {
      case "http://www.w3.org/2000/svg":
        return 1;
      case "http://www.w3.org/1998/Math/MathML":
        return 2;
      default:
        return 0;
    }
  }
  function Um(t, e) {
    if (t === 0)
      switch (e) {
        case "svg":
          return 1;
        case "math":
          return 2;
        default:
          return 0;
      }
    return t === 1 && e === "foreignObject" ? 0 : t;
  }
  function xr(t, e) {
    return t === "textarea" || t === "noscript" || typeof e.children == "string" || typeof e.children == "number" || typeof e.children == "bigint" || typeof e.dangerouslySetInnerHTML == "object" && e.dangerouslySetInnerHTML !== null && e.dangerouslySetInnerHTML.__html != null;
  }
  var Mr = null;
  function m1() {
    var t = window.event;
    return t && t.type === "popstate" ? t === Mr ? !1 : (Mr = t, !0) : (Mr = null, !1);
  }
  var Bm = typeof setTimeout == "function" ? setTimeout : void 0, y1 = typeof clearTimeout == "function" ? clearTimeout : void 0, Nm = typeof Promise == "function" ? Promise : void 0, p1 = typeof queueMicrotask == "function" ? queueMicrotask : typeof Nm < "u" ? function(t) {
    return Nm.resolve(null).then(t).catch(g1);
  } : Bm;
  function g1(t) {
    setTimeout(function() {
      throw t;
    });
  }
  function Hn(t) {
    return t === "head";
  }
  function jm(t, e) {
    var n = e, a = 0;
    do {
      var s = n.nextSibling;
      if (t.removeChild(n), s && s.nodeType === 8)
        if (n = s.data, n === "/$" || n === "/&") {
          if (a === 0) {
            t.removeChild(s), ia(e);
            return;
          }
          a--;
        } else if (n === "$" || n === "$?" || n === "$~" || n === "$!" || n === "&")
          a++;
        else if (n === "html")
          Ia(t.ownerDocument.documentElement);
        else if (n === "head") {
          n = t.ownerDocument.head, Ia(n);
          for (var r = n.firstChild; r; ) {
            var f = r.nextSibling, p = r.nodeName;
            r[ga] || p === "SCRIPT" || p === "STYLE" || p === "LINK" && r.rel.toLowerCase() === "stylesheet" || n.removeChild(r), r = f;
          }
        } else
          n === "body" && Ia(t.ownerDocument.body);
      n = s;
    } while (n);
    ia(e);
  }
  function wm(t, e) {
    var n = t;
    t = 0;
    do {
      var a = n.nextSibling;
      if (n.nodeType === 1 ? e ? (n._stashedDisplay = n.style.display, n.style.display = "none") : (n.style.display = n._stashedDisplay || "", n.getAttribute("style") === "" && n.removeAttribute("style")) : n.nodeType === 3 && (e ? (n._stashedText = n.nodeValue, n.nodeValue = "") : n.nodeValue = n._stashedText || ""), a && a.nodeType === 8)
        if (n = a.data, n === "/$") {
          if (t === 0) break;
          t--;
        } else
          n !== "$" && n !== "$?" && n !== "$~" && n !== "$!" || t++;
      n = a;
    } while (n);
  }
  function Dr(t) {
    var e = t.firstChild;
    for (e && e.nodeType === 10 && (e = e.nextSibling); e; ) {
      var n = e;
      switch (e = e.nextSibling, n.nodeName) {
        case "HTML":
        case "HEAD":
        case "BODY":
          Dr(n), Ou(n);
          continue;
        case "SCRIPT":
        case "STYLE":
          continue;
        case "LINK":
          if (n.rel.toLowerCase() === "stylesheet") continue;
      }
      t.removeChild(n);
    }
  }
  function v1(t, e, n, a) {
    for (; t.nodeType === 1; ) {
      var s = n;
      if (t.nodeName.toLowerCase() !== e.toLowerCase()) {
        if (!a && (t.nodeName !== "INPUT" || t.type !== "hidden"))
          break;
      } else if (a) {
        if (!t[ga])
          switch (e) {
            case "meta":
              if (!t.hasAttribute("itemprop")) break;
              return t;
            case "link":
              if (r = t.getAttribute("rel"), r === "stylesheet" && t.hasAttribute("data-precedence"))
                break;
              if (r !== s.rel || t.getAttribute("href") !== (s.href == null || s.href === "" ? null : s.href) || t.getAttribute("crossorigin") !== (s.crossOrigin == null ? null : s.crossOrigin) || t.getAttribute("title") !== (s.title == null ? null : s.title))
                break;
              return t;
            case "style":
              if (t.hasAttribute("data-precedence")) break;
              return t;
            case "script":
              if (r = t.getAttribute("src"), (r !== (s.src == null ? null : s.src) || t.getAttribute("type") !== (s.type == null ? null : s.type) || t.getAttribute("crossorigin") !== (s.crossOrigin == null ? null : s.crossOrigin)) && r && t.hasAttribute("async") && !t.hasAttribute("itemprop"))
                break;
              return t;
            default:
              return t;
          }
      } else if (e === "input" && t.type === "hidden") {
        var r = s.name == null ? null : "" + s.name;
        if (s.type === "hidden" && t.getAttribute("name") === r)
          return t;
      } else return t;
      if (t = je(t.nextSibling), t === null) break;
    }
    return null;
  }
  function S1(t, e, n) {
    if (e === "") return null;
    for (; t.nodeType !== 3; )
      if ((t.nodeType !== 1 || t.nodeName !== "INPUT" || t.type !== "hidden") && !n || (t = je(t.nextSibling), t === null)) return null;
    return t;
  }
  function Lm(t, e) {
    for (; t.nodeType !== 8; )
      if ((t.nodeType !== 1 || t.nodeName !== "INPUT" || t.type !== "hidden") && !e || (t = je(t.nextSibling), t === null)) return null;
    return t;
  }
  function Cr(t) {
    return t.data === "$?" || t.data === "$~";
  }
  function zr(t) {
    return t.data === "$!" || t.data === "$?" && t.ownerDocument.readyState !== "loading";
  }
  function T1(t, e) {
    var n = t.ownerDocument;
    if (t.data === "$~") t._reactRetry = e;
    else if (t.data !== "$?" || n.readyState !== "loading")
      e();
    else {
      var a = function() {
        e(), n.removeEventListener("DOMContentLoaded", a);
      };
      n.addEventListener("DOMContentLoaded", a), t._reactRetry = a;
    }
  }
  function je(t) {
    for (; t != null; t = t.nextSibling) {
      var e = t.nodeType;
      if (e === 1 || e === 3) break;
      if (e === 8) {
        if (e = t.data, e === "$" || e === "$!" || e === "$?" || e === "$~" || e === "&" || e === "F!" || e === "F")
          break;
        if (e === "/$" || e === "/&") return null;
      }
    }
    return t;
  }
  var Rr = null;
  function Hm(t) {
    t = t.nextSibling;
    for (var e = 0; t; ) {
      if (t.nodeType === 8) {
        var n = t.data;
        if (n === "/$" || n === "/&") {
          if (e === 0)
            return je(t.nextSibling);
          e--;
        } else
          n !== "$" && n !== "$!" && n !== "$?" && n !== "$~" && n !== "&" || e++;
      }
      t = t.nextSibling;
    }
    return null;
  }
  function Ym(t) {
    t = t.previousSibling;
    for (var e = 0; t; ) {
      if (t.nodeType === 8) {
        var n = t.data;
        if (n === "$" || n === "$!" || n === "$?" || n === "$~" || n === "&") {
          if (e === 0) return t;
          e--;
        } else n !== "/$" && n !== "/&" || e++;
      }
      t = t.previousSibling;
    }
    return null;
  }
  function qm(t, e, n) {
    switch (e = zs(n), t) {
      case "html":
        if (t = e.documentElement, !t) throw Error(o(452));
        return t;
      case "head":
        if (t = e.head, !t) throw Error(o(453));
        return t;
      case "body":
        if (t = e.body, !t) throw Error(o(454));
        return t;
      default:
        throw Error(o(451));
    }
  }
  function Ia(t) {
    for (var e = t.attributes; e.length; )
      t.removeAttributeNode(e[0]);
    Ou(t);
  }
  var we = /* @__PURE__ */ new Map(), Gm = /* @__PURE__ */ new Set();
  function Rs(t) {
    return typeof t.getRootNode == "function" ? t.getRootNode() : t.nodeType === 9 ? t : t.ownerDocument;
  }
  var vn = X.d;
  X.d = {
    f: b1,
    r: A1,
    D: E1,
    C: x1,
    L: M1,
    m: D1,
    X: z1,
    S: C1,
    M: R1
  };
  function b1() {
    var t = vn.f(), e = Ts();
    return t || e;
  }
  function A1(t) {
    var e = Ai(t);
    e !== null && e.tag === 5 && e.type === "form" ? ld(e) : vn.r(t);
  }
  var ta = typeof document > "u" ? null : document;
  function Xm(t, e, n) {
    var a = ta;
    if (a && typeof e == "string" && e) {
      var s = Re(e);
      s = 'link[rel="' + t + '"][href="' + s + '"]', typeof n == "string" && (s += '[crossorigin="' + n + '"]'), Gm.has(s) || (Gm.add(s), t = { rel: t, crossOrigin: n, href: e }, a.querySelector(s) === null && (e = a.createElement("link"), ne(e, "link", t), Ft(e), a.head.appendChild(e)));
    }
  }
  function E1(t) {
    vn.D(t), Xm("dns-prefetch", t, null);
  }
  function x1(t, e) {
    vn.C(t, e), Xm("preconnect", t, e);
  }
  function M1(t, e, n) {
    vn.L(t, e, n);
    var a = ta;
    if (a && t && e) {
      var s = 'link[rel="preload"][as="' + Re(e) + '"]';
      e === "image" && n && n.imageSrcSet ? (s += '[imagesrcset="' + Re(
        n.imageSrcSet
      ) + '"]', typeof n.imageSizes == "string" && (s += '[imagesizes="' + Re(
        n.imageSizes
      ) + '"]')) : s += '[href="' + Re(t) + '"]';
      var r = s;
      switch (e) {
        case "style":
          r = ea(t);
          break;
        case "script":
          r = na(t);
      }
      we.has(r) || (t = S(
        {
          rel: "preload",
          href: e === "image" && n && n.imageSrcSet ? void 0 : t,
          as: e
        },
        n
      ), we.set(r, t), a.querySelector(s) !== null || e === "style" && a.querySelector(tl(r)) || e === "script" && a.querySelector(el(r)) || (e = a.createElement("link"), ne(e, "link", t), Ft(e), a.head.appendChild(e)));
    }
  }
  function D1(t, e) {
    vn.m(t, e);
    var n = ta;
    if (n && t) {
      var a = e && typeof e.as == "string" ? e.as : "script", s = 'link[rel="modulepreload"][as="' + Re(a) + '"][href="' + Re(t) + '"]', r = s;
      switch (a) {
        case "audioworklet":
        case "paintworklet":
        case "serviceworker":
        case "sharedworker":
        case "worker":
        case "script":
          r = na(t);
      }
      if (!we.has(r) && (t = S({ rel: "modulepreload", href: t }, e), we.set(r, t), n.querySelector(s) === null)) {
        switch (a) {
          case "audioworklet":
          case "paintworklet":
          case "serviceworker":
          case "sharedworker":
          case "worker":
          case "script":
            if (n.querySelector(el(r)))
              return;
        }
        a = n.createElement("link"), ne(a, "link", t), Ft(a), n.head.appendChild(a);
      }
    }
  }
  function C1(t, e, n) {
    vn.S(t, e, n);
    var a = ta;
    if (a && t) {
      var s = Ei(a).hoistableStyles, r = ea(t);
      e = e || "default";
      var f = s.get(r);
      if (!f) {
        var p = { loading: 0, preload: null };
        if (f = a.querySelector(
          tl(r)
        ))
          p.loading = 5;
        else {
          t = S(
            { rel: "stylesheet", href: t, "data-precedence": e },
            n
          ), (n = we.get(r)) && Or(t, n);
          var T = f = a.createElement("link");
          Ft(T), ne(T, "link", t), T._p = new Promise(function(D, V) {
            T.onload = D, T.onerror = V;
          }), T.addEventListener("load", function() {
            p.loading |= 1;
          }), T.addEventListener("error", function() {
            p.loading |= 2;
          }), p.loading |= 4, Os(f, e, a);
        }
        f = {
          type: "stylesheet",
          instance: f,
          count: 1,
          state: p
        }, s.set(r, f);
      }
    }
  }
  function z1(t, e) {
    vn.X(t, e);
    var n = ta;
    if (n && t) {
      var a = Ei(n).hoistableScripts, s = na(t), r = a.get(s);
      r || (r = n.querySelector(el(s)), r || (t = S({ src: t, async: !0 }, e), (e = we.get(s)) && Vr(t, e), r = n.createElement("script"), Ft(r), ne(r, "link", t), n.head.appendChild(r)), r = {
        type: "script",
        instance: r,
        count: 1,
        state: null
      }, a.set(s, r));
    }
  }
  function R1(t, e) {
    vn.M(t, e);
    var n = ta;
    if (n && t) {
      var a = Ei(n).hoistableScripts, s = na(t), r = a.get(s);
      r || (r = n.querySelector(el(s)), r || (t = S({ src: t, async: !0, type: "module" }, e), (e = we.get(s)) && Vr(t, e), r = n.createElement("script"), Ft(r), ne(r, "link", t), n.head.appendChild(r)), r = {
        type: "script",
        instance: r,
        count: 1,
        state: null
      }, a.set(s, r));
    }
  }
  function Zm(t, e, n, a) {
    var s = (s = ct.current) ? Rs(s) : null;
    if (!s) throw Error(o(446));
    switch (t) {
      case "meta":
      case "title":
        return null;
      case "style":
        return typeof n.precedence == "string" && typeof n.href == "string" ? (e = ea(n.href), n = Ei(
          s
        ).hoistableStyles, a = n.get(e), a || (a = {
          type: "style",
          instance: null,
          count: 0,
          state: null
        }, n.set(e, a)), a) : { type: "void", instance: null, count: 0, state: null };
      case "link":
        if (n.rel === "stylesheet" && typeof n.href == "string" && typeof n.precedence == "string") {
          t = ea(n.href);
          var r = Ei(
            s
          ).hoistableStyles, f = r.get(t);
          if (f || (s = s.ownerDocument || s, f = {
            type: "stylesheet",
            instance: null,
            count: 0,
            state: { loading: 0, preload: null }
          }, r.set(t, f), (r = s.querySelector(
            tl(t)
          )) && !r._p && (f.instance = r, f.state.loading = 5), we.has(t) || (n = {
            rel: "preload",
            as: "style",
            href: n.href,
            crossOrigin: n.crossOrigin,
            integrity: n.integrity,
            media: n.media,
            hrefLang: n.hrefLang,
            referrerPolicy: n.referrerPolicy
          }, we.set(t, n), r || O1(
            s,
            t,
            n,
            f.state
          ))), e && a === null)
            throw Error(o(528, ""));
          return f;
        }
        if (e && a !== null)
          throw Error(o(529, ""));
        return null;
      case "script":
        return e = n.async, n = n.src, typeof n == "string" && e && typeof e != "function" && typeof e != "symbol" ? (e = na(n), n = Ei(
          s
        ).hoistableScripts, a = n.get(e), a || (a = {
          type: "script",
          instance: null,
          count: 0,
          state: null
        }, n.set(e, a)), a) : { type: "void", instance: null, count: 0, state: null };
      default:
        throw Error(o(444, t));
    }
  }
  function ea(t) {
    return 'href="' + Re(t) + '"';
  }
  function tl(t) {
    return 'link[rel="stylesheet"][' + t + "]";
  }
  function Qm(t) {
    return S({}, t, {
      "data-precedence": t.precedence,
      precedence: null
    });
  }
  function O1(t, e, n, a) {
    t.querySelector('link[rel="preload"][as="style"][' + e + "]") ? a.loading = 1 : (e = t.createElement("link"), a.preload = e, e.addEventListener("load", function() {
      return a.loading |= 1;
    }), e.addEventListener("error", function() {
      return a.loading |= 2;
    }), ne(e, "link", n), Ft(e), t.head.appendChild(e));
  }
  function na(t) {
    return '[src="' + Re(t) + '"]';
  }
  function el(t) {
    return "script[async]" + t;
  }
  function Km(t, e, n) {
    if (e.count++, e.instance === null)
      switch (e.type) {
        case "style":
          var a = t.querySelector(
            'style[data-href~="' + Re(n.href) + '"]'
          );
          if (a)
            return e.instance = a, Ft(a), a;
          var s = S({}, n, {
            "data-href": n.href,
            "data-precedence": n.precedence,
            href: null,
            precedence: null
          });
          return a = (t.ownerDocument || t).createElement(
            "style"
          ), Ft(a), ne(a, "style", s), Os(a, n.precedence, t), e.instance = a;
        case "stylesheet":
          s = ea(n.href);
          var r = t.querySelector(
            tl(s)
          );
          if (r)
            return e.state.loading |= 4, e.instance = r, Ft(r), r;
          a = Qm(n), (s = we.get(s)) && Or(a, s), r = (t.ownerDocument || t).createElement("link"), Ft(r);
          var f = r;
          return f._p = new Promise(function(p, T) {
            f.onload = p, f.onerror = T;
          }), ne(r, "link", a), e.state.loading |= 4, Os(r, n.precedence, t), e.instance = r;
        case "script":
          return r = na(n.src), (s = t.querySelector(
            el(r)
          )) ? (e.instance = s, Ft(s), s) : (a = n, (s = we.get(r)) && (a = S({}, n), Vr(a, s)), t = t.ownerDocument || t, s = t.createElement("script"), Ft(s), ne(s, "link", a), t.head.appendChild(s), e.instance = s);
        case "void":
          return null;
        default:
          throw Error(o(443, e.type));
      }
    else
      e.type === "stylesheet" && (e.state.loading & 4) === 0 && (a = e.instance, e.state.loading |= 4, Os(a, n.precedence, t));
    return e.instance;
  }
  function Os(t, e, n) {
    for (var a = n.querySelectorAll(
      'link[rel="stylesheet"][data-precedence],style[data-precedence]'
    ), s = a.length ? a[a.length - 1] : null, r = s, f = 0; f < a.length; f++) {
      var p = a[f];
      if (p.dataset.precedence === e) r = p;
      else if (r !== s) break;
    }
    r ? r.parentNode.insertBefore(t, r.nextSibling) : (e = n.nodeType === 9 ? n.head : n, e.insertBefore(t, e.firstChild));
  }
  function Or(t, e) {
    t.crossOrigin == null && (t.crossOrigin = e.crossOrigin), t.referrerPolicy == null && (t.referrerPolicy = e.referrerPolicy), t.title == null && (t.title = e.title);
  }
  function Vr(t, e) {
    t.crossOrigin == null && (t.crossOrigin = e.crossOrigin), t.referrerPolicy == null && (t.referrerPolicy = e.referrerPolicy), t.integrity == null && (t.integrity = e.integrity);
  }
  var Vs = null;
  function Jm(t, e, n) {
    if (Vs === null) {
      var a = /* @__PURE__ */ new Map(), s = Vs = /* @__PURE__ */ new Map();
      s.set(n, a);
    } else
      s = Vs, a = s.get(n), a || (a = /* @__PURE__ */ new Map(), s.set(n, a));
    if (a.has(t)) return a;
    for (a.set(t, null), n = n.getElementsByTagName(t), s = 0; s < n.length; s++) {
      var r = n[s];
      if (!(r[ga] || r[$t] || t === "link" && r.getAttribute("rel") === "stylesheet") && r.namespaceURI !== "http://www.w3.org/2000/svg") {
        var f = r.getAttribute(e) || "";
        f = t + f;
        var p = a.get(f);
        p ? p.push(r) : a.set(f, [r]);
      }
    }
    return a;
  }
  function km(t, e, n) {
    t = t.ownerDocument || t, t.head.insertBefore(
      n,
      e === "title" ? t.querySelector("head > title") : null
    );
  }
  function V1(t, e, n) {
    if (n === 1 || e.itemProp != null) return !1;
    switch (t) {
      case "meta":
      case "title":
        return !0;
      case "style":
        if (typeof e.precedence != "string" || typeof e.href != "string" || e.href === "")
          break;
        return !0;
      case "link":
        if (typeof e.rel != "string" || typeof e.href != "string" || e.href === "" || e.onLoad || e.onError)
          break;
        return e.rel === "stylesheet" ? (t = e.disabled, typeof e.precedence == "string" && t == null) : !0;
      case "script":
        if (e.async && typeof e.async != "function" && typeof e.async != "symbol" && !e.onLoad && !e.onError && e.src && typeof e.src == "string")
          return !0;
    }
    return !1;
  }
  function Fm(t) {
    return !(t.type === "stylesheet" && (t.state.loading & 3) === 0);
  }
  function _1(t, e, n, a) {
    if (n.type === "stylesheet" && (typeof a.media != "string" || matchMedia(a.media).matches !== !1) && (n.state.loading & 4) === 0) {
      if (n.instance === null) {
        var s = ea(a.href), r = e.querySelector(
          tl(s)
        );
        if (r) {
          e = r._p, e !== null && typeof e == "object" && typeof e.then == "function" && (t.count++, t = _s.bind(t), e.then(t, t)), n.state.loading |= 4, n.instance = r, Ft(r);
          return;
        }
        r = e.ownerDocument || e, a = Qm(a), (s = we.get(s)) && Or(a, s), r = r.createElement("link"), Ft(r);
        var f = r;
        f._p = new Promise(function(p, T) {
          f.onload = p, f.onerror = T;
        }), ne(r, "link", a), n.instance = r;
      }
      t.stylesheets === null && (t.stylesheets = /* @__PURE__ */ new Map()), t.stylesheets.set(n, e), (e = n.state.preload) && (n.state.loading & 3) === 0 && (t.count++, n = _s.bind(t), e.addEventListener("load", n), e.addEventListener("error", n));
    }
  }
  var _r = 0;
  function U1(t, e) {
    return t.stylesheets && t.count === 0 && Bs(t, t.stylesheets), 0 < t.count || 0 < t.imgCount ? function(n) {
      var a = setTimeout(function() {
        if (t.stylesheets && Bs(t, t.stylesheets), t.unsuspend) {
          var r = t.unsuspend;
          t.unsuspend = null, r();
        }
      }, 6e4 + e);
      0 < t.imgBytes && _r === 0 && (_r = 62500 * d1());
      var s = setTimeout(
        function() {
          if (t.waitingForImages = !1, t.count === 0 && (t.stylesheets && Bs(t, t.stylesheets), t.unsuspend)) {
            var r = t.unsuspend;
            t.unsuspend = null, r();
          }
        },
        (t.imgBytes > _r ? 50 : 800) + e
      );
      return t.unsuspend = n, function() {
        t.unsuspend = null, clearTimeout(a), clearTimeout(s);
      };
    } : null;
  }
  function _s() {
    if (this.count--, this.count === 0 && (this.imgCount === 0 || !this.waitingForImages)) {
      if (this.stylesheets) Bs(this, this.stylesheets);
      else if (this.unsuspend) {
        var t = this.unsuspend;
        this.unsuspend = null, t();
      }
    }
  }
  var Us = null;
  function Bs(t, e) {
    t.stylesheets = null, t.unsuspend !== null && (t.count++, Us = /* @__PURE__ */ new Map(), e.forEach(B1, t), Us = null, _s.call(t));
  }
  function B1(t, e) {
    if (!(e.state.loading & 4)) {
      var n = Us.get(t);
      if (n) var a = n.get(null);
      else {
        n = /* @__PURE__ */ new Map(), Us.set(t, n);
        for (var s = t.querySelectorAll(
          "link[data-precedence],style[data-precedence]"
        ), r = 0; r < s.length; r++) {
          var f = s[r];
          (f.nodeName === "LINK" || f.getAttribute("media") !== "not all") && (n.set(f.dataset.precedence, f), a = f);
        }
        a && n.set(null, a);
      }
      s = e.instance, f = s.getAttribute("data-precedence"), r = n.get(f) || a, r === a && n.set(null, s), n.set(f, s), this.count++, a = _s.bind(this), s.addEventListener("load", a), s.addEventListener("error", a), r ? r.parentNode.insertBefore(s, r.nextSibling) : (t = t.nodeType === 9 ? t.head : t, t.insertBefore(s, t.firstChild)), e.state.loading |= 4;
    }
  }
  var nl = {
    $$typeof: H,
    Provider: null,
    Consumer: null,
    _currentValue: J,
    _currentValue2: J,
    _threadCount: 0
  };
  function N1(t, e, n, a, s, r, f, p, T) {
    this.tag = 1, this.containerInfo = t, this.pingCache = this.current = this.pendingChildren = null, this.timeoutHandle = -1, this.callbackNode = this.next = this.pendingContext = this.context = this.cancelPendingCommit = null, this.callbackPriority = 0, this.expirationTimes = Du(-1), this.entangledLanes = this.shellSuspendCounter = this.errorRecoveryDisabledLanes = this.expiredLanes = this.warmLanes = this.pingedLanes = this.suspendedLanes = this.pendingLanes = 0, this.entanglements = Du(0), this.hiddenUpdates = Du(null), this.identifierPrefix = a, this.onUncaughtError = s, this.onCaughtError = r, this.onRecoverableError = f, this.pooledCache = null, this.pooledCacheLanes = 0, this.formState = T, this.incompleteTransitions = /* @__PURE__ */ new Map();
  }
  function Wm(t, e, n, a, s, r, f, p, T, D, V, B) {
    return t = new N1(
      t,
      e,
      n,
      f,
      T,
      D,
      V,
      B,
      p
    ), e = 1, r === !0 && (e |= 24), r = be(3, null, null, e), t.current = r, r.stateNode = t, e = co(), e.refCount++, t.pooledCache = e, e.refCount++, r.memoizedState = {
      element: a,
      isDehydrated: n,
      cache: e
    }, yo(r), t;
  }
  function Pm(t) {
    return t ? (t = Ui, t) : Ui;
  }
  function $m(t, e, n, a, s, r) {
    s = Pm(s), a.context === null ? a.context = s : a.pendingContext = s, a = zn(e), a.payload = { element: n }, r = r === void 0 ? null : r, r !== null && (a.callback = r), n = Rn(t, a, e), n !== null && (pe(n, t, e), Ba(n, t, e));
  }
  function Im(t, e) {
    if (t = t.memoizedState, t !== null && t.dehydrated !== null) {
      var n = t.retryLane;
      t.retryLane = n !== 0 && n < e ? n : e;
    }
  }
  function Ur(t, e) {
    Im(t, e), (t = t.alternate) && Im(t, e);
  }
  function ty(t) {
    if (t.tag === 13 || t.tag === 31) {
      var e = ei(t, 67108864);
      e !== null && pe(e, t, 67108864), Ur(t, 67108864);
    }
  }
  function ey(t) {
    if (t.tag === 13 || t.tag === 31) {
      var e = De();
      e = Cu(e);
      var n = ei(t, e);
      n !== null && pe(n, t, e), Ur(t, e);
    }
  }
  var Ns = !0;
  function j1(t, e, n, a) {
    var s = O.T;
    O.T = null;
    var r = X.p;
    try {
      X.p = 2, Br(t, e, n, a);
    } finally {
      X.p = r, O.T = s;
    }
  }
  function w1(t, e, n, a) {
    var s = O.T;
    O.T = null;
    var r = X.p;
    try {
      X.p = 8, Br(t, e, n, a);
    } finally {
      X.p = r, O.T = s;
    }
  }
  function Br(t, e, n, a) {
    if (Ns) {
      var s = Nr(a);
      if (s === null)
        Tr(
          t,
          e,
          a,
          js,
          n
        ), iy(t, a);
      else if (H1(
        s,
        t,
        e,
        n,
        a
      ))
        a.stopPropagation();
      else if (iy(t, a), e & 4 && -1 < L1.indexOf(t)) {
        for (; s !== null; ) {
          var r = Ai(s);
          if (r !== null)
            switch (r.tag) {
              case 3:
                if (r = r.stateNode, r.current.memoizedState.isDehydrated) {
                  var f = Wn(r.pendingLanes);
                  if (f !== 0) {
                    var p = r;
                    for (p.pendingLanes |= 2, p.entangledLanes |= 2; f; ) {
                      var T = 1 << 31 - Se(f);
                      p.entanglements[1] |= T, f &= ~T;
                    }
                    Fe(r), (bt & 6) === 0 && (vs = ge() + 500, Wa(0));
                  }
                }
                break;
              case 31:
              case 13:
                p = ei(r, 2), p !== null && pe(p, r, 2), Ts(), Ur(r, 2);
            }
          if (r = Nr(a), r === null && Tr(
            t,
            e,
            a,
            js,
            n
          ), r === s) break;
          s = r;
        }
        s !== null && a.stopPropagation();
      } else
        Tr(
          t,
          e,
          a,
          null,
          n
        );
    }
  }
  function Nr(t) {
    return t = ju(t), jr(t);
  }
  var js = null;
  function jr(t) {
    if (js = null, t = bi(t), t !== null) {
      var e = d(t);
      if (e === null) t = null;
      else {
        var n = e.tag;
        if (n === 13) {
          if (t = h(e), t !== null) return t;
          t = null;
        } else if (n === 31) {
          if (t = y(e), t !== null) return t;
          t = null;
        } else if (n === 3) {
          if (e.stateNode.current.memoizedState.isDehydrated)
            return e.tag === 3 ? e.stateNode.containerInfo : null;
          t = null;
        } else e !== t && (t = null);
      }
    }
    return js = t, null;
  }
  function ny(t) {
    switch (t) {
      case "beforetoggle":
      case "cancel":
      case "click":
      case "close":
      case "contextmenu":
      case "copy":
      case "cut":
      case "auxclick":
      case "dblclick":
      case "dragend":
      case "dragstart":
      case "drop":
      case "focusin":
      case "focusout":
      case "input":
      case "invalid":
      case "keydown":
      case "keypress":
      case "keyup":
      case "mousedown":
      case "mouseup":
      case "paste":
      case "pause":
      case "play":
      case "pointercancel":
      case "pointerdown":
      case "pointerup":
      case "ratechange":
      case "reset":
      case "resize":
      case "seeked":
      case "submit":
      case "toggle":
      case "touchcancel":
      case "touchend":
      case "touchstart":
      case "volumechange":
      case "change":
      case "selectionchange":
      case "textInput":
      case "compositionstart":
      case "compositionend":
      case "compositionupdate":
      case "beforeblur":
      case "afterblur":
      case "beforeinput":
      case "blur":
      case "fullscreenchange":
      case "focus":
      case "hashchange":
      case "popstate":
      case "select":
      case "selectstart":
        return 2;
      case "drag":
      case "dragenter":
      case "dragexit":
      case "dragleave":
      case "dragover":
      case "mousemove":
      case "mouseout":
      case "mouseover":
      case "pointermove":
      case "pointerout":
      case "pointerover":
      case "scroll":
      case "touchmove":
      case "wheel":
      case "mouseenter":
      case "mouseleave":
      case "pointerenter":
      case "pointerleave":
        return 8;
      case "message":
        switch (E0()) {
          case cf:
            return 2;
          case ff:
            return 8;
          case Ml:
          case x0:
            return 32;
          case hf:
            return 268435456;
          default:
            return 32;
        }
      default:
        return 32;
    }
  }
  var wr = !1, Yn = null, qn = null, Gn = null, il = /* @__PURE__ */ new Map(), al = /* @__PURE__ */ new Map(), Xn = [], L1 = "mousedown mouseup touchcancel touchend touchstart auxclick dblclick pointercancel pointerdown pointerup dragend dragstart drop compositionend compositionstart keydown keypress keyup input textInput copy cut paste click change contextmenu reset".split(
    " "
  );
  function iy(t, e) {
    switch (t) {
      case "focusin":
      case "focusout":
        Yn = null;
        break;
      case "dragenter":
      case "dragleave":
        qn = null;
        break;
      case "mouseover":
      case "mouseout":
        Gn = null;
        break;
      case "pointerover":
      case "pointerout":
        il.delete(e.pointerId);
        break;
      case "gotpointercapture":
      case "lostpointercapture":
        al.delete(e.pointerId);
    }
  }
  function ll(t, e, n, a, s, r) {
    return t === null || t.nativeEvent !== r ? (t = {
      blockedOn: e,
      domEventName: n,
      eventSystemFlags: a,
      nativeEvent: r,
      targetContainers: [s]
    }, e !== null && (e = Ai(e), e !== null && ty(e)), t) : (t.eventSystemFlags |= a, e = t.targetContainers, s !== null && e.indexOf(s) === -1 && e.push(s), t);
  }
  function H1(t, e, n, a, s) {
    switch (e) {
      case "focusin":
        return Yn = ll(
          Yn,
          t,
          e,
          n,
          a,
          s
        ), !0;
      case "dragenter":
        return qn = ll(
          qn,
          t,
          e,
          n,
          a,
          s
        ), !0;
      case "mouseover":
        return Gn = ll(
          Gn,
          t,
          e,
          n,
          a,
          s
        ), !0;
      case "pointerover":
        var r = s.pointerId;
        return il.set(
          r,
          ll(
            il.get(r) || null,
            t,
            e,
            n,
            a,
            s
          )
        ), !0;
      case "gotpointercapture":
        return r = s.pointerId, al.set(
          r,
          ll(
            al.get(r) || null,
            t,
            e,
            n,
            a,
            s
          )
        ), !0;
    }
    return !1;
  }
  function ay(t) {
    var e = bi(t.target);
    if (e !== null) {
      var n = d(e);
      if (n !== null) {
        if (e = n.tag, e === 13) {
          if (e = h(n), e !== null) {
            t.blockedOn = e, vf(t.priority, function() {
              ey(n);
            });
            return;
          }
        } else if (e === 31) {
          if (e = y(n), e !== null) {
            t.blockedOn = e, vf(t.priority, function() {
              ey(n);
            });
            return;
          }
        } else if (e === 3 && n.stateNode.current.memoizedState.isDehydrated) {
          t.blockedOn = n.tag === 3 ? n.stateNode.containerInfo : null;
          return;
        }
      }
    }
    t.blockedOn = null;
  }
  function ws(t) {
    if (t.blockedOn !== null) return !1;
    for (var e = t.targetContainers; 0 < e.length; ) {
      var n = Nr(t.nativeEvent);
      if (n === null) {
        n = t.nativeEvent;
        var a = new n.constructor(
          n.type,
          n
        );
        Nu = a, n.target.dispatchEvent(a), Nu = null;
      } else
        return e = Ai(n), e !== null && ty(e), t.blockedOn = n, !1;
      e.shift();
    }
    return !0;
  }
  function ly(t, e, n) {
    ws(t) && n.delete(e);
  }
  function Y1() {
    wr = !1, Yn !== null && ws(Yn) && (Yn = null), qn !== null && ws(qn) && (qn = null), Gn !== null && ws(Gn) && (Gn = null), il.forEach(ly), al.forEach(ly);
  }
  function Ls(t, e) {
    t.blockedOn === e && (t.blockedOn = null, wr || (wr = !0, i.unstable_scheduleCallback(
      i.unstable_NormalPriority,
      Y1
    )));
  }
  var Hs = null;
  function sy(t) {
    Hs !== t && (Hs = t, i.unstable_scheduleCallback(
      i.unstable_NormalPriority,
      function() {
        Hs === t && (Hs = null);
        for (var e = 0; e < t.length; e += 3) {
          var n = t[e], a = t[e + 1], s = t[e + 2];
          if (typeof a != "function") {
            if (jr(a || n) === null)
              continue;
            break;
          }
          var r = Ai(n);
          r !== null && (t.splice(e, 3), e -= 3, No(
            r,
            {
              pending: !0,
              data: s,
              method: n.method,
              action: a
            },
            a,
            s
          ));
        }
      }
    ));
  }
  function ia(t) {
    function e(T) {
      return Ls(T, t);
    }
    Yn !== null && Ls(Yn, t), qn !== null && Ls(qn, t), Gn !== null && Ls(Gn, t), il.forEach(e), al.forEach(e);
    for (var n = 0; n < Xn.length; n++) {
      var a = Xn[n];
      a.blockedOn === t && (a.blockedOn = null);
    }
    for (; 0 < Xn.length && (n = Xn[0], n.blockedOn === null); )
      ay(n), n.blockedOn === null && Xn.shift();
    if (n = (t.ownerDocument || t).$$reactFormReplay, n != null)
      for (a = 0; a < n.length; a += 3) {
        var s = n[a], r = n[a + 1], f = s[ce] || null;
        if (typeof r == "function")
          f || sy(n);
        else if (f) {
          var p = null;
          if (r && r.hasAttribute("formAction")) {
            if (s = r, f = r[ce] || null)
              p = f.formAction;
            else if (jr(s) !== null) continue;
          } else p = f.action;
          typeof p == "function" ? n[a + 1] = p : (n.splice(a, 3), a -= 3), sy(n);
        }
      }
  }
  function uy() {
    function t(r) {
      r.canIntercept && r.info === "react-transition" && r.intercept({
        handler: function() {
          return new Promise(function(f) {
            return s = f;
          });
        },
        focusReset: "manual",
        scroll: "manual"
      });
    }
    function e() {
      s !== null && (s(), s = null), a || setTimeout(n, 20);
    }
    function n() {
      if (!a && !navigation.transition) {
        var r = navigation.currentEntry;
        r && r.url != null && navigation.navigate(r.url, {
          state: r.getState(),
          info: "react-transition",
          history: "replace"
        });
      }
    }
    if (typeof navigation == "object") {
      var a = !1, s = null;
      return navigation.addEventListener("navigate", t), navigation.addEventListener("navigatesuccess", e), navigation.addEventListener("navigateerror", e), setTimeout(n, 100), function() {
        a = !0, navigation.removeEventListener("navigate", t), navigation.removeEventListener("navigatesuccess", e), navigation.removeEventListener("navigateerror", e), s !== null && (s(), s = null);
      };
    }
  }
  function Lr(t) {
    this._internalRoot = t;
  }
  Ys.prototype.render = Lr.prototype.render = function(t) {
    var e = this._internalRoot;
    if (e === null) throw Error(o(409));
    var n = e.current, a = De();
    $m(n, a, t, e, null, null);
  }, Ys.prototype.unmount = Lr.prototype.unmount = function() {
    var t = this._internalRoot;
    if (t !== null) {
      this._internalRoot = null;
      var e = t.containerInfo;
      $m(t.current, 2, null, t, null, null), Ts(), e[Ti] = null;
    }
  };
  function Ys(t) {
    this._internalRoot = t;
  }
  Ys.prototype.unstable_scheduleHydration = function(t) {
    if (t) {
      var e = gf();
      t = { blockedOn: null, target: t, priority: e };
      for (var n = 0; n < Xn.length && e !== 0 && e < Xn[n].priority; n++) ;
      Xn.splice(n, 0, t), n === 0 && ay(t);
    }
  };
  var oy = l.version;
  if (oy !== "19.2.8")
    throw Error(
      o(
        527,
        oy,
        "19.2.8"
      )
    );
  X.findDOMNode = function(t) {
    var e = t._reactInternals;
    if (e === void 0)
      throw typeof t.render == "function" ? Error(o(188)) : (t = Object.keys(t).join(","), Error(o(268, t)));
    return t = m(e), t = t !== null ? v(t) : null, t = t === null ? null : t.stateNode, t;
  };
  var q1 = {
    bundleType: 0,
    version: "19.2.8",
    rendererPackageName: "react-dom",
    currentDispatcherRef: O,
    reconcilerVersion: "19.2.8"
  };
  if (typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ < "u") {
    var qs = __REACT_DEVTOOLS_GLOBAL_HOOK__;
    if (!qs.isDisabled && qs.supportsFiber)
      try {
        ma = qs.inject(
          q1
        ), ve = qs;
      } catch {
      }
  }
  return ul.createRoot = function(t, e) {
    if (!c(t)) throw Error(o(299));
    var n = !1, a = "", s = yd, r = pd, f = gd;
    return e != null && (e.unstable_strictMode === !0 && (n = !0), e.identifierPrefix !== void 0 && (a = e.identifierPrefix), e.onUncaughtError !== void 0 && (s = e.onUncaughtError), e.onCaughtError !== void 0 && (r = e.onCaughtError), e.onRecoverableError !== void 0 && (f = e.onRecoverableError)), e = Wm(
      t,
      1,
      !1,
      null,
      null,
      n,
      a,
      null,
      s,
      r,
      f,
      uy
    ), t[Ti] = e.current, Sr(t), new Lr(e);
  }, ul.hydrateRoot = function(t, e, n) {
    if (!c(t)) throw Error(o(299));
    var a = !1, s = "", r = yd, f = pd, p = gd, T = null;
    return n != null && (n.unstable_strictMode === !0 && (a = !0), n.identifierPrefix !== void 0 && (s = n.identifierPrefix), n.onUncaughtError !== void 0 && (r = n.onUncaughtError), n.onCaughtError !== void 0 && (f = n.onCaughtError), n.onRecoverableError !== void 0 && (p = n.onRecoverableError), n.formState !== void 0 && (T = n.formState)), e = Wm(
      t,
      1,
      !0,
      e,
      n ?? null,
      a,
      s,
      T,
      r,
      f,
      p,
      uy
    ), e.context = Pm(null), n = e.current, a = De(), a = Cu(a), s = zn(a), s.callback = null, Rn(n, s, a), n = a, e.current.lanes = n, pa(e, n), Fe(e), t[Ti] = e.current, Sr(t), new Ys(e);
  }, ul.version = "19.2.8", ul;
}
var vy;
function P1() {
  if (vy) return qr.exports;
  vy = 1;
  function i() {
    if (!(typeof __REACT_DEVTOOLS_GLOBAL_HOOK__ > "u" || typeof __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE != "function"))
      try {
        __REACT_DEVTOOLS_GLOBAL_HOOK__.checkDCE(i);
      } catch (l) {
        console.error(l);
      }
  }
  return i(), qr.exports = W1(), qr.exports;
}
var $1 = P1();
const I1 = (i) => i.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase(), jp = (...i) => i.filter((l, u, o) => !!l && l.trim() !== "" && o.indexOf(l) === u).join(" ").trim();
var tS = {
  xmlns: "http://www.w3.org/2000/svg",
  width: 24,
  height: 24,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 2,
  strokeLinecap: "round",
  strokeLinejoin: "round"
};
const eS = q.forwardRef(
  ({
    color: i = "currentColor",
    size: l = 24,
    strokeWidth: u = 2,
    absoluteStrokeWidth: o,
    className: c = "",
    children: d,
    iconNode: h,
    ...y
  }, g) => q.createElement(
    "svg",
    {
      ref: g,
      ...tS,
      width: l,
      height: l,
      stroke: i,
      strokeWidth: o ? Number(u) * 24 / Number(l) : u,
      className: jp("lucide", c),
      ...y
    },
    [
      ...h.map(([m, v]) => q.createElement(m, v)),
      ...Array.isArray(d) ? d : [d]
    ]
  )
);
const Sl = (i, l) => {
  const u = q.forwardRef(
    ({ className: o, ...c }, d) => q.createElement(eS, {
      ref: d,
      iconNode: l,
      className: jp(`lucide-${I1(i)}`, o),
      ...c
    })
  );
  return u.displayName = `${i}`, u;
};
const nS = Sl("ArrowLeftRight", [
  ["path", { d: "M8 3 4 7l4 4", key: "9rb6wj" }],
  ["path", { d: "M4 7h16", key: "6tx8e3" }],
  ["path", { d: "m16 21 4-4-4-4", key: "siv7j2" }],
  ["path", { d: "M20 17H4", key: "h6l3hr" }]
]);
const iS = Sl("FileCheck2", [
  ["path", { d: "M4 22h14a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v4", key: "1pf5j1" }],
  ["path", { d: "M14 2v4a2 2 0 0 0 2 2h4", key: "tnqrlb" }],
  ["path", { d: "m3 15 2 2 4-4", key: "1lhrkk" }]
]);
const aS = Sl("FileText", [
  ["path", { d: "M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z", key: "1rqfz7" }],
  ["path", { d: "M14 2v4a2 2 0 0 0 2 2h4", key: "tnqrlb" }],
  ["path", { d: "M10 9H8", key: "b1mrlr" }],
  ["path", { d: "M16 13H8", key: "t4e002" }],
  ["path", { d: "M16 17H8", key: "z1uh3a" }]
]);
const lS = Sl("Landmark", [
  ["line", { x1: "3", x2: "21", y1: "22", y2: "22", key: "j8o0r" }],
  ["line", { x1: "6", x2: "6", y1: "18", y2: "11", key: "10tf0k" }],
  ["line", { x1: "10", x2: "10", y1: "18", y2: "11", key: "54lgf6" }],
  ["line", { x1: "14", x2: "14", y1: "18", y2: "11", key: "380y" }],
  ["line", { x1: "18", x2: "18", y1: "18", y2: "11", key: "1kevvc" }],
  ["polygon", { points: "12 2 20 7 4 7", key: "jkujk7" }]
]);
const sS = Sl("SlidersHorizontal", [
  ["line", { x1: "21", x2: "14", y1: "4", y2: "4", key: "obuewd" }],
  ["line", { x1: "10", x2: "3", y1: "4", y2: "4", key: "1q6298" }],
  ["line", { x1: "21", x2: "12", y1: "12", y2: "12", key: "1iu8h1" }],
  ["line", { x1: "8", x2: "3", y1: "12", y2: "12", key: "ntss68" }],
  ["line", { x1: "21", x2: "16", y1: "20", y2: "20", key: "14d8ph" }],
  ["line", { x1: "12", x2: "3", y1: "20", y2: "20", key: "m0wm8r" }],
  ["line", { x1: "14", x2: "14", y1: "2", y2: "6", key: "14e1ph" }],
  ["line", { x1: "8", x2: "8", y1: "10", y2: "14", key: "1i6ji0" }],
  ["line", { x1: "16", x2: "16", y1: "18", y2: "22", key: "1lctlv" }]
]), Uc = q.createContext({});
function du(i) {
  const l = q.useRef(null);
  return l.current === null && (l.current = i()), l.current;
}
const uS = typeof window < "u", Bc = uS ? q.useLayoutEffect : q.useEffect, mu = /* @__PURE__ */ q.createContext(null);
function Nc(i, l) {
  i.indexOf(l) === -1 && i.push(l);
}
function iu(i, l) {
  const u = i.indexOf(l);
  u > -1 && i.splice(u, 1);
}
const Ie = (i, l, u) => u > l ? l : u < i ? i : u;
let yu = () => {
};
const Kn = {}, wp = (i) => /^-?(?:\d+(?:\.\d+)?|\.\d+)$/u.test(i), Lp = (i) => typeof i == "object" && i !== null, Hp = (i) => /^0[^.\s]+$/u.test(i);
// @__NO_SIDE_EFFECTS__
function Yp(i) {
  let l;
  return () => (l === void 0 && (l = i()), l);
}
const He = /* @__NO_SIDE_EFFECTS__ */ (i) => i, Tl = (...i) => i.reduce((l, u) => (o) => u(l(o))), ml = /* @__NO_SIDE_EFFECTS__ */ (i, l, u) => {
  const o = l - i;
  return o ? (u - i) / o : 1;
};
class jc {
  constructor() {
    this.subscriptions = [];
  }
  add(l) {
    return Nc(this.subscriptions, l), () => iu(this.subscriptions, l);
  }
  notify(l, u, o) {
    const c = this.subscriptions.length;
    if (c)
      if (c === 1)
        this.subscriptions[0](l, u, o);
      else
        for (let d = 0; d < c; d++) {
          const h = this.subscriptions[d];
          h && h(l, u, o);
        }
  }
  getSize() {
    return this.subscriptions.length;
  }
  clear() {
    this.subscriptions.length = 0;
  }
}
const Ce = /* @__NO_SIDE_EFFECTS__ */ (i) => i * 1e3, Le = /* @__NO_SIDE_EFFECTS__ */ (i) => i / 1e3, qp = /* @__NO_SIDE_EFFECTS__ */ (i, l) => l ? i * (1e3 / l) : 0, Gp = (i, l, u) => (((1 - 3 * u + 3 * l) * i + (3 * u - 6 * l)) * i + 3 * l) * i, oS = 1e-7, rS = 12;
function cS(i, l, u, o, c) {
  let d, h, y = 0;
  do
    h = l + (u - l) / 2, d = Gp(h, o, c) - i, d > 0 ? u = h : l = h;
  while (Math.abs(d) > oS && ++y < rS);
  return h;
}
// @__NO_SIDE_EFFECTS__
function bl(i, l, u, o) {
  if (i === l && u === o)
    return He;
  const c = (d) => cS(d, 0, 1, i, u);
  return (d) => d === 0 || d === 1 ? d : Gp(c(d), l, o);
}
const Xp = /* @__NO_SIDE_EFFECTS__ */ (i) => (l) => l <= 0.5 ? i(2 * l) / 2 : (2 - i(2 * (1 - l))) / 2, Zp = /* @__NO_SIDE_EFFECTS__ */ (i) => (l) => 1 - i(1 - l), Qp = /* @__PURE__ */ bl(0.33, 1.53, 0.69, 0.99), wc = /* @__PURE__ */ Zp(Qp), Kp = /* @__PURE__ */ Xp(wc), Jp = (i) => i >= 1 ? 1 : (i *= 2) < 1 ? 0.5 * wc(i) : 0.5 * (2 - Math.pow(2, -10 * (i - 1))), Lc = (i) => 1 - Math.sin(Math.acos(i)), kp = /* @__PURE__ */ Zp(Lc), Fp = /* @__PURE__ */ Xp(Lc), fS = /* @__PURE__ */ bl(0.42, 0, 1, 1), hS = /* @__PURE__ */ bl(0, 0, 0.58, 1), Wp = /* @__PURE__ */ bl(0.42, 0, 0.58, 1), dS = /* @__NO_SIDE_EFFECTS__ */ (i) => Array.isArray(i) && typeof i[0] != "number", Pp = /* @__NO_SIDE_EFFECTS__ */ (i) => Array.isArray(i) && typeof i[0] == "number", mS = {
  linear: He,
  easeIn: fS,
  easeInOut: Wp,
  easeOut: hS,
  circIn: Lc,
  circInOut: Fp,
  circOut: kp,
  backIn: wc,
  backInOut: Kp,
  backOut: Qp,
  anticipate: Jp
}, yS = (i) => typeof i == "string", Sy = (i) => {
  if (/* @__PURE__ */ Pp(i)) {
    yu(i.length === 4);
    const [l, u, o, c] = i;
    return /* @__PURE__ */ bl(l, u, o, c);
  } else if (yS(i))
    return mS[i];
  return i;
}, Gs = [
  "setup",
  // Compute
  "read",
  // Read
  "resolveKeyframes",
  // Write/Read/Write/Read
  "preUpdate",
  // Compute
  "update",
  // Compute
  "preRender",
  // Compute
  "render",
  // Write
  "postRender"
  // Compute
];
function pS(i) {
  let l = /* @__PURE__ */ new Set(), u = /* @__PURE__ */ new Set(), o = !1, c = !1;
  const d = /* @__PURE__ */ new WeakSet();
  let h = {
    delta: 0,
    timestamp: 0,
    isProcessing: !1
  };
  function y(m) {
    d.has(m) && (g.schedule(m), i()), m(h);
  }
  const g = {
    /**
     * Schedule a process to run on the next frame.
     */
    schedule: (m, v = !1, S = !1) => {
      const _ = S && o ? l : u;
      return v && d.add(m), _.add(m), m;
    },
    /**
     * Cancel the provided callback from running on the next frame.
     */
    cancel: (m) => {
      u.delete(m), d.delete(m);
    },
    /**
     * Execute all schedule callbacks.
     */
    process: (m) => {
      if (h = m, o) {
        c = !0;
        return;
      }
      o = !0;
      const v = l;
      l = u, u = v, l.forEach(y), l.clear(), o = !1, c && (c = !1, g.process(m));
    }
  };
  return g;
}
const gS = 40;
function $p(i, l) {
  let u = !1, o = !0;
  const c = {
    delta: 0,
    timestamp: 0,
    isProcessing: !1
  }, d = () => u = !0, h = Gs.reduce((H, Y) => (H[Y] = pS(d), H), {}), { setup: y, read: g, resolveKeyframes: m, preUpdate: v, update: S, preRender: b, render: _, postRender: z } = h, j = () => {
    const H = Kn.useManualTiming, Y = H ? c.timestamp : performance.now();
    u = !1, H || (c.delta = o ? 1e3 / 60 : Math.max(Math.min(Y - c.timestamp, gS), 1)), c.timestamp = Y, c.isProcessing = !0, y.process(c), g.process(c), m.process(c), v.process(c), S.process(c), b.process(c), _.process(c), z.process(c), c.isProcessing = !1, u && l && (o = !1, i(j));
  }, w = () => {
    u = !0, o = !0, c.isProcessing || i(j);
  };
  return { schedule: Gs.reduce((H, Y) => {
    const tt = h[Y];
    return H[Y] = (nt, Q = !1, K = !1) => (u || w(), tt.schedule(nt, Q, K)), H;
  }, {}), cancel: (H) => {
    for (let Y = 0; Y < Gs.length; Y++)
      h[Gs[Y]].cancel(H);
  }, state: c, steps: h };
}
const { schedule: Ot, cancel: Jn, state: ie, steps: Qr } = /* @__PURE__ */ $p(typeof requestAnimationFrame < "u" ? requestAnimationFrame : He, !0);
let ks;
function vS() {
  ks = void 0;
}
const oe = {
  now: () => (ks === void 0 && oe.set(ie.isProcessing || Kn.useManualTiming ? ie.timestamp : performance.now()), ks),
  set: (i) => {
    ks = i, queueMicrotask(vS);
  }
}, Ip = (i) => (l) => typeof l == "string" && l.startsWith(i), tg = /* @__PURE__ */ Ip("--"), SS = /* @__PURE__ */ Ip("var(--"), Hc = (i) => SS(i) ? TS.test(i.split("/*")[0].trim()) : !1, TS = /var\(--(?:[\w-]+\s*|[\w-]+\s*,(?:\s*[^)(\s]|\s*\((?:[^)(]|\([^)(]*\))*\))+\s*)\)$/iu;
function Ty(i) {
  return typeof i != "string" ? !1 : i.split("/*")[0].includes("var(--");
}
const ca = {
  test: (i) => typeof i == "number",
  parse: parseFloat,
  transform: (i) => i
}, yl = {
  ...ca,
  transform: (i) => Ie(0, 1, i)
}, Xs = {
  ...ca,
  default: 1
}, cl = (i) => Math.round(i * 1e5) / 1e5, Yc = /-?(?:\d+(?:\.\d+)?|\.\d+)/gu;
function bS(i) {
  return i == null;
}
const AS = /^(?:#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\))$/iu, qc = (i, l) => (u) => !!(typeof u == "string" && AS.test(u) && u.startsWith(i) || l && !bS(u) && Object.prototype.hasOwnProperty.call(u, l)), eg = (i, l, u) => (o) => {
  if (typeof o != "string")
    return o;
  const [c, d, h, y] = o.match(Yc);
  return {
    [i]: parseFloat(c),
    [l]: parseFloat(d),
    [u]: parseFloat(h),
    alpha: y !== void 0 ? parseFloat(y) : 1
  };
}, ES = (i) => Ie(0, 255, i), Kr = {
  ...ca,
  transform: (i) => Math.round(ES(i))
}, pi = {
  test: /* @__PURE__ */ qc("rgb", "red"),
  parse: /* @__PURE__ */ eg("red", "green", "blue"),
  transform: ({ red: i, green: l, blue: u, alpha: o = 1 }) => "rgba(" + Kr.transform(i) + ", " + Kr.transform(l) + ", " + Kr.transform(u) + ", " + cl(yl.transform(o)) + ")"
};
function xS(i) {
  let l = "", u = "", o = "", c = "";
  return i.length > 5 ? (l = i.substring(1, 3), u = i.substring(3, 5), o = i.substring(5, 7), c = i.substring(7, 9)) : (l = i.substring(1, 2), u = i.substring(2, 3), o = i.substring(3, 4), c = i.substring(4, 5), l += l, u += u, o += o, c += c), {
    red: parseInt(l, 16),
    green: parseInt(u, 16),
    blue: parseInt(o, 16),
    alpha: c ? parseInt(c, 16) / 255 : 1
  };
}
const uc = {
  test: /* @__PURE__ */ qc("#"),
  parse: xS,
  transform: pi.transform
}, Al = /* @__NO_SIDE_EFFECTS__ */ (i) => ({
  test: (l) => typeof l == "string" && l.endsWith(i) && l.split(" ").length === 1,
  parse: parseFloat,
  transform: (l) => `${l}${i}`
}), Sn = /* @__PURE__ */ Al("deg"), $e = /* @__PURE__ */ Al("%"), F = /* @__PURE__ */ Al("px"), MS = /* @__PURE__ */ Al("vh"), DS = /* @__PURE__ */ Al("vw"), by = {
  ...$e,
  parse: (i) => $e.parse(i) / 100,
  transform: (i) => $e.transform(i * 100)
}, la = {
  test: /* @__PURE__ */ qc("hsl", "hue"),
  parse: /* @__PURE__ */ eg("hue", "saturation", "lightness"),
  transform: ({ hue: i, saturation: l, lightness: u, alpha: o = 1 }) => "hsla(" + Math.round(i) + ", " + $e.transform(cl(l)) + ", " + $e.transform(cl(u)) + ", " + cl(yl.transform(o)) + ")"
}, Kt = {
  test: (i) => pi.test(i) || uc.test(i) || la.test(i),
  parse: (i) => pi.test(i) ? pi.parse(i) : la.test(i) ? la.parse(i) : uc.parse(i),
  transform: (i) => typeof i == "string" ? i : i.hasOwnProperty("red") ? pi.transform(i) : la.transform(i),
  getAnimatableNone: (i) => {
    const l = Kt.parse(i);
    return l.alpha = 0, Kt.transform(l);
  }
}, CS = /(?:#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\))/giu;
function zS(i) {
  return isNaN(i) && typeof i == "string" && (i.match(Yc)?.length || 0) + (i.match(CS)?.length || 0) > 0;
}
const ng = "number", ig = "color", RS = "var", OS = "var(", Ay = "${}", VS = /var\s*\(\s*--(?:[\w-]+\s*|[\w-]+\s*,(?:\s*[^)(\s]|\s*\((?:[^)(]|\([^)(]*\))*\))+\s*)\)|#[\da-f]{3,8}|(?:rgb|hsl)a?\((?:-?[\d.]+%?[,\s]+){2}-?[\d.]+%?\s*(?:[,/]\s*)?(?:\b\d+(?:\.\d+)?|\.\d+)?%?\)|-?(?:\d+(?:\.\d+)?|\.\d+)/giu;
function oa(i) {
  const l = i.toString(), u = [], o = {
    color: [],
    number: [],
    var: []
  }, c = [];
  let d = 0;
  const y = l.replace(VS, (g) => (Kt.test(g) ? (o.color.push(d), c.push(ig), u.push(Kt.parse(g))) : g.startsWith(OS) ? (o.var.push(d), c.push(RS), u.push(g)) : (o.number.push(d), c.push(ng), u.push(parseFloat(g))), ++d, Ay)).split(Ay);
  return { values: u, split: y, indexes: o, types: c };
}
function _S(i) {
  return oa(i).values;
}
function ag({ split: i, types: l }) {
  const u = i.length;
  return (o) => {
    let c = "";
    for (let d = 0; d < u; d++)
      if (c += i[d], o[d] !== void 0) {
        const h = l[d];
        h === ng ? c += cl(o[d]) : h === ig ? c += Kt.transform(o[d]) : c += o[d];
      }
    return c;
  };
}
function US(i) {
  return ag(oa(i));
}
const BS = (i) => typeof i == "number" ? 0 : Kt.test(i) ? Kt.getAnimatableNone(i) : i, NS = (i, l) => typeof i == "number" ? l?.trim().endsWith("/") ? i : 0 : BS(i);
function jS(i) {
  const l = oa(i);
  return ag(l)(l.values.map((o, c) => NS(o, l.split[c])));
}
const Qe = {
  test: zS,
  parse: _S,
  createTransformer: US,
  getAnimatableNone: jS
};
function Jr(i, l, u) {
  return u < 0 && (u += 1), u > 1 && (u -= 1), u < 1 / 6 ? i + (l - i) * 6 * u : u < 1 / 2 ? l : u < 2 / 3 ? i + (l - i) * (2 / 3 - u) * 6 : i;
}
function wS({ hue: i, saturation: l, lightness: u, alpha: o }) {
  i /= 360, l /= 100, u /= 100;
  let c = 0, d = 0, h = 0;
  if (!l)
    c = d = h = u;
  else {
    const y = u < 0.5 ? u * (1 + l) : u + l - u * l, g = 2 * u - y;
    c = Jr(g, y, i + 1 / 3), d = Jr(g, y, i), h = Jr(g, y, i - 1 / 3);
  }
  return {
    red: Math.round(c * 255),
    green: Math.round(d * 255),
    blue: Math.round(h * 255),
    alpha: o
  };
}
function au(i, l) {
  return (u) => u > 0 ? l : i;
}
const Rt = (i, l, u) => i + (l - i) * u, kr = (i, l, u) => {
  const o = i * i, c = u * (l * l - o) + o;
  return c < 0 ? 0 : Math.sqrt(c);
}, LS = [uc, pi, la], HS = (i) => LS.find((l) => l.test(i));
function Ey(i) {
  const l = HS(i);
  if (!l)
    return !1;
  let u = l.parse(i);
  return l === la && (u = wS(u)), u;
}
const xy = (i, l) => {
  const u = Ey(i), o = Ey(l);
  if (!u || !o)
    return au(i, l);
  const c = { ...u };
  return (d) => (c.red = kr(u.red, o.red, d), c.green = kr(u.green, o.green, d), c.blue = kr(u.blue, o.blue, d), c.alpha = Rt(u.alpha, o.alpha, d), pi.transform(c));
}, oc = /* @__PURE__ */ new Set(["none", "hidden"]);
function YS(i, l) {
  return oc.has(i) ? (u) => u <= 0 ? i : l : (u) => u >= 1 ? l : i;
}
function qS(i, l) {
  return (u) => Rt(i, l, u);
}
function Gc(i) {
  return typeof i == "number" ? qS : typeof i == "string" ? Hc(i) ? au : Kt.test(i) ? xy : ZS : Array.isArray(i) ? lg : typeof i == "object" ? Kt.test(i) ? xy : GS : au;
}
function lg(i, l) {
  const u = [...i], o = u.length, c = i.map((d, h) => Gc(d)(d, l[h]));
  return (d) => {
    for (let h = 0; h < o; h++)
      u[h] = c[h](d);
    return u;
  };
}
function GS(i, l) {
  const u = { ...i, ...l }, o = {};
  for (const c in u)
    i[c] !== void 0 && l[c] !== void 0 && (o[c] = Gc(i[c])(i[c], l[c]));
  return (c) => {
    for (const d in o)
      u[d] = o[d](c);
    return u;
  };
}
function XS(i, l) {
  const u = [], o = { color: 0, var: 0, number: 0 };
  for (let c = 0; c < l.values.length; c++) {
    const d = l.types[c], h = i.indexes[d][o[d]], y = i.values[h] ?? 0;
    u[c] = y, o[d]++;
  }
  return u;
}
const ZS = (i, l) => {
  const u = Qe.createTransformer(l), o = oa(i), c = oa(l);
  return o.indexes.var.length === c.indexes.var.length && o.indexes.color.length === c.indexes.color.length && o.indexes.number.length >= c.indexes.number.length ? oc.has(i) && !c.values.length || oc.has(l) && !o.values.length ? YS(i, l) : Tl(lg(XS(o, c), c.values), u) : au(i, l);
};
function sg(i, l, u) {
  return typeof i == "number" && typeof l == "number" && typeof u == "number" ? Rt(i, l, u) : Gc(i)(i, l);
}
const QS = (i) => {
  const l = ({ timestamp: u }) => i(u);
  return {
    start: (u = !0) => Ot.update(l, u),
    stop: () => Jn(l),
    /**
     * If we're processing this frame we can use the
     * framelocked timestamp to keep things in sync.
     */
    now: () => ie.isProcessing ? ie.timestamp : oe.now()
  };
}, ug = (i, l, u = 10) => {
  let o = "";
  const c = Math.max(Math.round(l / u), 2);
  for (let d = 0; d < c; d++)
    o += Math.round(i(d / (c - 1)) * 1e4) / 1e4 + ", ";
  return `linear(${o.substring(0, o.length - 2)})`;
}, lu = 2e4;
function Xc(i) {
  let l = 0;
  const u = 50;
  let o = i.next(l);
  for (; !o.done && l < lu; )
    l += u, o = i.next(l);
  return l >= lu ? 1 / 0 : l;
}
function KS(i, l = 100, u) {
  const o = u({ ...i, keyframes: [0, l] }), c = Math.min(Xc(o), lu);
  return {
    type: "keyframes",
    ease: (d) => o.next(c * d).value / l,
    duration: /* @__PURE__ */ Le(c)
  };
}
const jt = {
  // Default spring physics
  stiffness: 100,
  damping: 10,
  mass: 1,
  velocity: 0,
  // Default duration/bounce-based options
  duration: 800,
  // in ms
  bounce: 0.3,
  visualDuration: 0.3,
  // in seconds
  // Rest thresholds
  restSpeed: {
    granular: 0.01,
    default: 2
  },
  restDelta: {
    granular: 5e-3,
    default: 0.5
  },
  // Limits
  minDuration: 0.01,
  // in seconds
  maxDuration: 10,
  // in seconds
  minDamping: 0.05,
  maxDamping: 1
};
function rc(i, l) {
  return i * Math.sqrt(1 - l * l);
}
const JS = 12;
function kS(i, l, u) {
  let o = u;
  for (let c = 1; c < JS; c++)
    o = o - i(o) / l(o);
  return o;
}
const Fr = 1e-3;
function FS({ duration: i = jt.duration, bounce: l = jt.bounce, velocity: u = jt.velocity, mass: o = jt.mass }) {
  let c, d, h = 1 - l;
  h = Ie(jt.minDamping, jt.maxDamping, h), i = Ie(jt.minDuration, jt.maxDuration, /* @__PURE__ */ Le(i)), h < 1 ? (c = (m) => {
    const v = m * h, S = v * i, b = v - u, _ = rc(m, h), z = Math.exp(-S);
    return Fr - b / _ * z;
  }, d = (m) => {
    const S = m * h * i, b = S * u + u, _ = Math.pow(h, 2) * Math.pow(m, 2) * i, z = Math.exp(-S), j = rc(Math.pow(m, 2), h);
    return (-c(m) + Fr > 0 ? -1 : 1) * ((b - _) * z) / j;
  }) : (c = (m) => {
    const v = Math.exp(-m * i), S = (m - u) * i + 1;
    return -Fr + v * S;
  }, d = (m) => {
    const v = Math.exp(-m * i), S = (u - m) * (i * i);
    return v * S;
  });
  const y = 5 / i, g = kS(c, d, y);
  if (i = /* @__PURE__ */ Ce(i), isNaN(g))
    return {
      stiffness: jt.stiffness,
      damping: jt.damping,
      duration: i
    };
  {
    const m = Math.pow(g, 2) * o;
    return {
      stiffness: m,
      damping: h * 2 * Math.sqrt(o * m),
      duration: i
    };
  }
}
const WS = ["duration", "bounce"], PS = ["stiffness", "damping", "mass"];
function My(i, l) {
  return l.some((u) => i[u] !== void 0);
}
function $S(i) {
  let l = {
    velocity: jt.velocity,
    stiffness: jt.stiffness,
    damping: jt.damping,
    mass: jt.mass,
    isResolvedFromDuration: !1,
    ...i
  };
  if (!My(i, PS) && My(i, WS))
    if (l.velocity = 0, i.visualDuration) {
      const u = i.visualDuration, o = 2 * Math.PI / (u * 1.2), c = o * o, d = 2 * Ie(0.05, 1, 1 - (i.bounce || 0)) * Math.sqrt(c);
      l = {
        ...l,
        mass: jt.mass,
        stiffness: c,
        damping: d
      };
    } else {
      const u = FS({ ...i, velocity: 0 });
      l = {
        ...l,
        ...u,
        mass: jt.mass
      }, l.isResolvedFromDuration = !0;
    }
  return l;
}
function su(i = jt.visualDuration, l = jt.bounce) {
  const u = typeof i != "object" ? {
    visualDuration: i,
    keyframes: [0, 1],
    bounce: l
  } : i;
  let { restSpeed: o, restDelta: c } = u;
  const d = u.keyframes[0], h = u.keyframes[u.keyframes.length - 1], y = { done: !1, value: d }, { stiffness: g, damping: m, mass: v, duration: S, velocity: b, isResolvedFromDuration: _ } = $S({
    ...u,
    velocity: -/* @__PURE__ */ Le(u.velocity || 0)
  }), z = b || 0, j = m / (2 * Math.sqrt(g * v)), w = h - d, L = /* @__PURE__ */ Le(Math.sqrt(g / v)), G = Math.abs(w) < 5;
  o || (o = G ? jt.restSpeed.granular : jt.restSpeed.default), c || (c = G ? jt.restDelta.granular : jt.restDelta.default);
  let H, Y, tt, nt, Q, K;
  if (j < 1)
    tt = rc(L, j), nt = (z + j * L * w) / tt, H = ($) => {
      const yt = Math.exp(-j * L * $);
      return h - yt * (nt * Math.sin(tt * $) + w * Math.cos(tt * $));
    }, Q = j * L * nt + w * tt, K = j * L * w - nt * tt, Y = ($) => Math.exp(-j * L * $) * (Q * Math.sin(tt * $) + K * Math.cos(tt * $));
  else if (j === 1) {
    H = (yt) => h - Math.exp(-L * yt) * (w + (z + L * w) * yt);
    const $ = z + L * w;
    Y = (yt) => Math.exp(-L * yt) * (L * $ * yt - z);
  } else {
    const $ = L * Math.sqrt(j * j - 1);
    H = (qt) => {
      const wt = Math.exp(-j * L * qt), O = Math.min($ * qt, 300);
      return h - wt * ((z + j * L * w) * Math.sinh(O) + $ * w * Math.cosh(O)) / $;
    };
    const yt = (z + j * L * w) / $, vt = j * L * yt - w * $, Pt = j * L * w - yt * $;
    Y = (qt) => {
      const wt = Math.exp(-j * L * qt), O = Math.min($ * qt, 300);
      return wt * (vt * Math.sinh(O) + Pt * Math.cosh(O));
    };
  }
  const it = {
    calculatedDuration: _ && S || null,
    velocity: ($) => /* @__PURE__ */ Ce(Y($)),
    next: ($) => {
      if (!_ && j < 1) {
        const vt = Math.exp(-j * L * $), Pt = Math.sin(tt * $), qt = Math.cos(tt * $), wt = h - vt * (nt * Pt + w * qt), O = /* @__PURE__ */ Ce(vt * (Q * Pt + K * qt));
        return y.done = Math.abs(O) <= o && Math.abs(h - wt) <= c, y.value = y.done ? h : wt, y;
      }
      const yt = H($);
      if (_)
        y.done = $ >= S;
      else {
        const vt = /* @__PURE__ */ Ce(Y($));
        y.done = Math.abs(vt) <= o && Math.abs(h - yt) <= c;
      }
      return y.value = y.done ? h : yt, y;
    },
    toString: () => {
      const $ = Math.min(Xc(it), lu), yt = ug((vt) => it.next($ * vt).value, $, 30);
      return $ + "ms " + yt;
    },
    toTransition: () => {
    }
  };
  return it;
}
su.applyToOptions = (i) => {
  const l = KS(i, 100, su);
  return i.ease = l.ease, i.duration = /* @__PURE__ */ Ce(l.duration), i.type = "keyframes", i;
};
const IS = 5;
function og(i, l, u) {
  const o = Math.max(l - IS, 0);
  return /* @__PURE__ */ qp(u - i(o), l - o);
}
function cc({ keyframes: i, velocity: l = 0, power: u = 0.8, timeConstant: o = 325, bounceDamping: c = 10, bounceStiffness: d = 500, modifyTarget: h, min: y, max: g, restDelta: m = 0.5, restSpeed: v }) {
  const S = i[0], b = {
    done: !1,
    value: S
  }, _ = (K) => y !== void 0 && K < y || g !== void 0 && K > g, z = (K) => y === void 0 ? g : g === void 0 || Math.abs(y - K) < Math.abs(g - K) ? y : g;
  let j = u * l;
  const w = S + j, L = h === void 0 ? w : h(w);
  L !== w && (j = L - S);
  const G = (K) => -j * Math.exp(-K / o), H = (K) => L + G(K), Y = (K) => {
    const it = G(K), $ = H(K);
    b.done = Math.abs(it) <= m, b.value = b.done ? L : $;
  };
  let tt, nt;
  const Q = (K) => {
    _(b.value) && (tt = K, nt = su({
      keyframes: [b.value, z(b.value)],
      velocity: og(H, K, b.value),
      // TODO: This should be passing * 1000
      damping: c,
      stiffness: d,
      restDelta: m,
      restSpeed: v
    }));
  };
  return Q(0), {
    calculatedDuration: null,
    next: (K) => {
      let it = !1;
      return !nt && tt === void 0 && (it = !0, Y(K), Q(K)), tt !== void 0 && K >= tt ? nt.next(K - tt) : (!it && Y(K), b);
    }
  };
}
function tT(i, l, u) {
  const o = [], c = u || Kn.mix || sg, d = i.length - 1;
  for (let h = 0; h < d; h++) {
    let y = c(i[h], i[h + 1]);
    if (l) {
      const g = Array.isArray(l) ? l[h] || He : l;
      y = Tl(g, y);
    }
    o.push(y);
  }
  return o;
}
function eT(i, l, { clamp: u = !0, ease: o, mixer: c } = {}) {
  const d = i.length;
  if (yu(d === l.length), d === 1)
    return () => l[0];
  if (d === 2 && l[0] === l[1])
    return () => l[1];
  const h = i[0] === i[1];
  i[0] > i[d - 1] && (i = [...i].reverse(), l = [...l].reverse());
  const y = tT(l, o, c), g = y.length, m = (v) => {
    if (h && v < i[0])
      return l[0];
    let S = 0;
    if (g > 1)
      for (; S < i.length - 2 && !(v < i[S + 1]); S++)
        ;
    const b = /* @__PURE__ */ ml(i[S], i[S + 1], v);
    return y[S](b);
  };
  return u ? (v) => m(Ie(i[0], i[d - 1], v)) : m;
}
function nT(i, l) {
  const u = i[i.length - 1];
  for (let o = 1; o <= l; o++) {
    const c = /* @__PURE__ */ ml(0, l, o);
    i.push(Rt(u, 1, c));
  }
}
function iT(i) {
  const l = [0];
  return nT(l, i.length - 1), l;
}
function aT(i, l) {
  return i.map((u) => u * l);
}
function lT(i, l) {
  return i.map(() => l || Wp).splice(0, i.length - 1);
}
function fl({ duration: i = 300, keyframes: l, times: u, ease: o = "easeInOut" }) {
  const c = /* @__PURE__ */ dS(o) ? o.map(Sy) : Sy(o), d = {
    done: !1,
    value: l[0]
  }, h = aT(
    // Only use the provided offsets if they're the correct length
    // TODO Maybe we should warn here if there's a length mismatch
    u && u.length === l.length ? u : iT(l),
    i
  ), y = eT(h, l, {
    ease: Array.isArray(c) ? c : lT(l, c)
  });
  return {
    calculatedDuration: i,
    next: (g) => (d.value = y(g), d.done = g >= i, d)
  };
}
const sT = (i) => i !== null;
function pu(i, { repeat: l, repeatType: u = "loop" }, o, c = 1) {
  const d = i.filter(sT), y = c < 0 || l && u !== "loop" && l % 2 === 1 ? 0 : d.length - 1;
  return !y || o === void 0 ? d[y] : o;
}
const uT = {
  decay: cc,
  inertia: cc,
  tween: fl,
  keyframes: fl,
  spring: su
};
function rg(i) {
  typeof i.type == "string" && (i.type = uT[i.type]);
}
class Zc {
  constructor() {
    this.updateFinished();
  }
  get finished() {
    return this._finished;
  }
  updateFinished() {
    this._finished = new Promise((l) => {
      this.resolve = l;
    });
  }
  notifyFinished() {
    this.resolve();
  }
  /**
   * Allows the animation to be awaited.
   *
   * @deprecated Use `finished` instead.
   */
  then(l, u) {
    return this.finished.then(l, u);
  }
}
const oT = (i) => i / 100;
class uu extends Zc {
  constructor(l) {
    super(), this.state = "idle", this.startTime = null, this.isStopped = !1, this.currentTime = 0, this.holdTime = null, this.playbackSpeed = 1, this.delayState = {
      done: !1,
      value: void 0
    }, this.stop = () => {
      const { motionValue: u } = this.options;
      u && u.updatedAt !== oe.now() && this.tick(oe.now()), this.isStopped = !0, this.state !== "idle" && (this.teardown(), this.options.onStop?.());
    }, this.options = l, this.initAnimation(), this.play(), l.autoplay === !1 && this.pause();
  }
  initAnimation() {
    const { options: l } = this;
    rg(l);
    const { type: u = fl, repeat: o = 0, repeatDelay: c = 0, repeatType: d, velocity: h = 0 } = l;
    let { keyframes: y } = l;
    const g = u || fl;
    g !== fl && typeof y[0] != "number" && (this.mixKeyframes = Tl(oT, sg(y[0], y[1])), y = [0, 100]);
    const m = g({ ...l, keyframes: y });
    d === "mirror" && (this.mirroredGenerator = g({
      ...l,
      keyframes: [...y].reverse(),
      velocity: -h
    })), m.calculatedDuration === null && (m.calculatedDuration = Xc(m));
    const { calculatedDuration: v } = m;
    this.calculatedDuration = v, this.resolvedDuration = v + c, this.totalDuration = this.resolvedDuration * (o + 1) - c, this.generator = m;
  }
  updateTime(l) {
    const u = Math.round(l - this.startTime) * this.playbackSpeed;
    this.holdTime !== null ? this.currentTime = this.holdTime : this.currentTime = u;
  }
  tick(l, u = !1) {
    const { generator: o, totalDuration: c, mixKeyframes: d, mirroredGenerator: h, resolvedDuration: y, calculatedDuration: g } = this;
    if (this.startTime === null)
      return o.next(0);
    const { delay: m = 0, keyframes: v, repeat: S, repeatType: b, repeatDelay: _, type: z, onUpdate: j, finalKeyframe: w } = this.options;
    this.speed > 0 ? this.startTime = Math.min(this.startTime, l) : this.speed < 0 && (this.startTime = Math.min(l - c / this.speed, this.startTime)), u ? this.currentTime = l : this.updateTime(l);
    const L = this.currentTime - m * (this.playbackSpeed >= 0 ? 1 : -1), G = this.playbackSpeed >= 0 ? L < 0 : L > c;
    this.currentTime = Math.max(L, 0), this.state === "finished" && this.holdTime === null && (this.currentTime = c);
    let H = this.currentTime, Y = o;
    if (S) {
      const K = Math.min(this.currentTime, c) / y;
      let it = Math.floor(K), $ = K % 1;
      !$ && K >= 1 && ($ = 1), $ === 1 && it--, it = Math.min(it, S + 1), it % 2 && (b === "reverse" ? ($ = 1 - $, _ && ($ -= _ / y)) : b === "mirror" && (Y = h)), H = Ie(0, 1, $) * y;
    }
    let tt;
    G ? (this.delayState.value = v[0], tt = this.delayState) : tt = Y.next(H), d && !G && (tt.value = d(tt.value));
    let { done: nt } = tt;
    !G && g !== null && (nt = this.playbackSpeed >= 0 ? this.currentTime >= c : this.currentTime <= 0);
    const Q = this.holdTime === null && (this.state === "finished" || this.state === "running" && nt);
    return Q && z !== cc && (tt.value = pu(v, this.options, w, this.speed)), j && j(tt.value), Q && this.finish(), tt;
  }
  /**
   * Allows the returned animation to be awaited or promise-chained. Currently
   * resolves when the animation finishes at all but in a future update could/should
   * reject if its cancels.
   */
  then(l, u) {
    return this.finished.then(l, u);
  }
  get duration() {
    return /* @__PURE__ */ Le(this.calculatedDuration);
  }
  get iterationDuration() {
    const { delay: l = 0 } = this.options || {};
    return this.duration + /* @__PURE__ */ Le(l);
  }
  get time() {
    return /* @__PURE__ */ Le(this.currentTime);
  }
  set time(l) {
    l = /* @__PURE__ */ Ce(l), this.currentTime = l, this.startTime === null || this.holdTime !== null || this.playbackSpeed === 0 ? this.holdTime = l : this.driver && (this.startTime = this.driver.now() - l / this.playbackSpeed), this.driver ? this.driver.start(!1) : (this.startTime = 0, this.state = "paused", this.holdTime = l, this.tick(l));
  }
  /**
   * Returns the generator's velocity at the current time in units/second.
   * Uses the analytical derivative when available (springs), avoiding
   * the MotionValue's frame-dependent velocity estimation.
   */
  getGeneratorVelocity() {
    const l = this.currentTime;
    if (l <= 0)
      return this.options.velocity || 0;
    if (this.generator.velocity)
      return this.generator.velocity(l);
    const u = this.generator.next(l).value;
    return og((o) => this.generator.next(o).value, l, u);
  }
  get speed() {
    return this.playbackSpeed;
  }
  set speed(l) {
    const u = this.playbackSpeed !== l;
    u && this.driver && this.updateTime(oe.now()), this.playbackSpeed = l, u && this.driver && (this.time = /* @__PURE__ */ Le(this.currentTime));
  }
  play() {
    if (this.isStopped)
      return;
    const { driver: l = QS, startTime: u } = this.options;
    this.driver || (this.driver = l((c) => this.tick(c))), this.options.onPlay?.();
    const o = this.driver.now();
    this.state === "finished" ? (this.updateFinished(), this.startTime = o) : this.holdTime !== null ? this.startTime = o - this.holdTime : this.startTime || (this.startTime = u ?? o), this.state === "finished" && this.speed < 0 && (this.startTime += this.calculatedDuration), this.holdTime = null, this.state = "running", this.driver.start();
  }
  pause() {
    this.state = "paused", this.updateTime(oe.now()), this.holdTime = this.currentTime;
  }
  complete() {
    this.state !== "running" && this.play(), this.state = "finished", this.holdTime = null;
  }
  finish() {
    this.notifyFinished(), this.teardown(), this.state = "finished", this.options.onComplete?.();
  }
  cancel() {
    this.holdTime = null, this.startTime = 0, this.tick(0), this.teardown(), this.options.onCancel?.();
  }
  teardown() {
    this.state = "idle", this.stopDriver(), this.startTime = this.holdTime = null;
  }
  stopDriver() {
    this.driver && (this.driver.stop(), this.driver = void 0);
  }
  sample(l) {
    return this.startTime = 0, this.tick(l, !0);
  }
  attachTimeline(l) {
    return this.options.allowFlatten && (this.options.type = "keyframes", this.options.ease = "linear", this.initAnimation()), this.driver?.stop(), l.observe(this);
  }
}
function rT(i) {
  for (let l = 1; l < i.length; l++)
    i[l] ?? (i[l] = i[l - 1]);
}
const gi = (i) => i * 180 / Math.PI, fc = (i) => {
  const l = gi(Math.atan2(i[1], i[0]));
  return hc(l);
}, cT = {
  x: 4,
  y: 5,
  translateX: 4,
  translateY: 5,
  scaleX: 0,
  scaleY: 3,
  scale: (i) => (Math.abs(i[0]) + Math.abs(i[3])) / 2,
  rotate: fc,
  rotateZ: fc,
  skewX: (i) => gi(Math.atan(i[1])),
  skewY: (i) => gi(Math.atan(i[2])),
  skew: (i) => (Math.abs(i[1]) + Math.abs(i[2])) / 2
}, hc = (i) => (i = i % 360, i < 0 && (i += 360), i), Dy = fc, Cy = (i) => Math.sqrt(i[0] * i[0] + i[1] * i[1]), zy = (i) => Math.sqrt(i[4] * i[4] + i[5] * i[5]), fT = {
  x: 12,
  y: 13,
  z: 14,
  translateX: 12,
  translateY: 13,
  translateZ: 14,
  scaleX: Cy,
  scaleY: zy,
  scale: (i) => (Cy(i) + zy(i)) / 2,
  rotateX: (i) => hc(gi(Math.atan2(i[6], i[5]))),
  rotateY: (i) => hc(gi(Math.atan2(-i[2], i[0]))),
  rotateZ: Dy,
  rotate: Dy,
  skewX: (i) => gi(Math.atan(i[4])),
  skewY: (i) => gi(Math.atan(i[1])),
  skew: (i) => (Math.abs(i[1]) + Math.abs(i[4])) / 2
};
function dc(i) {
  return i.includes("scale") ? 1 : 0;
}
function mc(i, l) {
  if (!i || i === "none")
    return dc(l);
  const u = i.match(/^matrix3d\(([-\d.e\s,]+)\)$/u);
  let o, c;
  if (u)
    o = fT, c = u;
  else {
    const y = i.match(/^matrix\(([-\d.e\s,]+)\)$/u);
    o = cT, c = y;
  }
  if (!c)
    return dc(l);
  const d = o[l], h = c[1].split(",").map(dT);
  return typeof d == "function" ? d(h) : h[d];
}
const hT = (i, l) => {
  const { transform: u = "none" } = getComputedStyle(i);
  return mc(u, l);
};
function dT(i) {
  return parseFloat(i.trim());
}
const fa = [
  "transformPerspective",
  "x",
  "y",
  "z",
  "translateX",
  "translateY",
  "translateZ",
  "scale",
  "scaleX",
  "scaleY",
  "rotate",
  "rotateX",
  "rotateY",
  "rotateZ",
  "skew",
  "skewX",
  "skewY"
], ha = /* @__PURE__ */ new Set([...fa, "pathRotation"]), Ry = (i) => i === ca || i === F, mT = /* @__PURE__ */ new Set(["x", "y", "z"]), yT = fa.filter((i) => !mT.has(i));
function pT(i) {
  const l = [];
  return yT.forEach((u) => {
    const o = i.getValue(u);
    o !== void 0 && (l.push([u, o.get()]), o.set(u.startsWith("scale") ? 1 : 0));
  }), l;
}
const Qn = {
  // Dimensions
  width: ({ x: i }, { paddingLeft: l = "0", paddingRight: u = "0", boxSizing: o }) => {
    const c = i.max - i.min;
    return o === "border-box" ? c : c - parseFloat(l) - parseFloat(u);
  },
  height: ({ y: i }, { paddingTop: l = "0", paddingBottom: u = "0", boxSizing: o }) => {
    const c = i.max - i.min;
    return o === "border-box" ? c : c - parseFloat(l) - parseFloat(u);
  },
  top: (i, { top: l }) => parseFloat(l),
  left: (i, { left: l }) => parseFloat(l),
  bottom: ({ y: i }, { top: l }) => parseFloat(l) + (i.max - i.min),
  right: ({ x: i }, { left: l }) => parseFloat(l) + (i.max - i.min),
  // Transform
  x: (i, { transform: l }) => mc(l, "x"),
  y: (i, { transform: l }) => mc(l, "y")
};
Qn.translateX = Qn.x;
Qn.translateY = Qn.y;
const vi = /* @__PURE__ */ new Set();
let yc = !1, pc = !1, gc = !1;
function cg() {
  if (pc) {
    const i = Array.from(vi).filter((o) => o.needsMeasurement), l = new Set(i.map((o) => o.element)), u = /* @__PURE__ */ new Map();
    l.forEach((o) => {
      const c = pT(o);
      c.length && (u.set(o, c), o.render());
    }), i.forEach((o) => o.measureInitialState()), l.forEach((o) => {
      o.render();
      const c = u.get(o);
      c && c.forEach(([d, h]) => {
        o.getValue(d)?.set(h);
      });
    }), i.forEach((o) => o.measureEndState()), i.forEach((o) => {
      o.suspendedScrollY !== void 0 && window.scrollTo(0, o.suspendedScrollY);
    });
  }
  pc = !1, yc = !1, vi.forEach((i) => i.complete(gc)), vi.clear();
}
function fg() {
  vi.forEach((i) => {
    i.readKeyframes(), i.needsMeasurement && (pc = !0);
  });
}
function gT() {
  gc = !0, fg(), cg(), gc = !1;
}
class Qc {
  constructor(l, u, o, c, d, h = !1) {
    this.state = "pending", this.isAsync = !1, this.needsMeasurement = !1, this.unresolvedKeyframes = [...l], this.onComplete = u, this.name = o, this.motionValue = c, this.element = d, this.isAsync = h;
  }
  scheduleResolve() {
    this.state = "scheduled", this.isAsync ? (vi.add(this), yc || (yc = !0, Ot.read(fg), Ot.resolveKeyframes(cg))) : (this.readKeyframes(), this.complete());
  }
  readKeyframes() {
    const { unresolvedKeyframes: l, name: u, element: o, motionValue: c } = this;
    if (l[0] === null) {
      const d = c?.get(), h = l[l.length - 1];
      if (d !== void 0)
        l[0] = d;
      else if (o && u) {
        const y = o.readValue(u, h);
        y != null && (l[0] = y);
      }
      l[0] === void 0 && (l[0] = h), c && d === void 0 && c.set(l[0]);
    }
    rT(l);
  }
  setFinalKeyframe() {
  }
  measureInitialState() {
  }
  renderEndStyles() {
  }
  measureEndState() {
  }
  complete(l = !1) {
    this.state = "complete", this.onComplete(this.unresolvedKeyframes, this.finalKeyframe, l), vi.delete(this);
  }
  cancel() {
    this.state === "scheduled" && (vi.delete(this), this.state = "pending");
  }
  resume() {
    this.state === "pending" && this.scheduleResolve();
  }
}
const vT = (i) => i.startsWith("--");
function hg(i, l, u) {
  vT(l) ? i.style.setProperty(l, u) : i.style[l] = u;
}
const ST = {};
function dg(i, l) {
  const u = /* @__PURE__ */ Yp(i);
  return () => ST[l] ?? u();
}
const TT = /* @__PURE__ */ dg(() => window.ScrollTimeline !== void 0, "scrollTimeline"), mg = /* @__PURE__ */ dg(() => {
  try {
    document.createElement("div").animate({ opacity: 0 }, { easing: "linear(0, 1)" });
  } catch {
    return !1;
  }
  return !0;
}, "linearEasing"), rl = ([i, l, u, o]) => `cubic-bezier(${i}, ${l}, ${u}, ${o})`, Oy = {
  linear: "linear",
  ease: "ease",
  easeIn: "ease-in",
  easeOut: "ease-out",
  easeInOut: "ease-in-out",
  circIn: /* @__PURE__ */ rl([0, 0.65, 0.55, 1]),
  circOut: /* @__PURE__ */ rl([0.55, 0, 1, 0.45]),
  backIn: /* @__PURE__ */ rl([0.31, 0.01, 0.66, -0.59]),
  backOut: /* @__PURE__ */ rl([0.33, 1.53, 0.69, 0.99])
};
function yg(i, l) {
  if (i)
    return typeof i == "function" ? mg() ? ug(i, l) : "ease-out" : /* @__PURE__ */ Pp(i) ? rl(i) : Array.isArray(i) ? i.map((u) => yg(u, l) || Oy.easeOut) : Oy[i];
}
function bT(i, l, u, { delay: o = 0, duration: c = 300, repeat: d = 0, repeatType: h = "loop", ease: y = "easeOut", times: g } = {}, m = void 0) {
  const v = {
    [l]: u
  };
  g && (v.offset = g);
  const S = yg(y, c);
  Array.isArray(S) && (v.easing = S);
  const b = {
    delay: o,
    duration: c,
    easing: Array.isArray(S) ? "linear" : S,
    fill: "both",
    iterations: d + 1,
    direction: h === "reverse" ? "alternate" : "normal"
  };
  return m && (b.pseudoElement = m), i.animate(v, b);
}
function pg(i) {
  return typeof i == "function" && "applyToOptions" in i;
}
function AT({ type: i, ...l }) {
  return pg(i) && mg() ? i.applyToOptions(l) : (l.duration ?? (l.duration = 300), l.ease ?? (l.ease = "easeOut"), l);
}
class gg extends Zc {
  constructor(l) {
    if (super(), this.finishedTime = null, this.isStopped = !1, this.manualStartTime = null, !l)
      return;
    const { element: u, name: o, keyframes: c, pseudoElement: d, allowFlatten: h = !1, finalKeyframe: y, onComplete: g } = l;
    this.isPseudoElement = !!d, this.allowFlatten = h, this.options = l, yu(typeof l.type != "string");
    const m = AT(l);
    this.animation = bT(u, o, c, m, d), m.autoplay === !1 && this.animation.pause(), this.animation.onfinish = () => {
      if (this.finishedTime = this.time, !d) {
        const v = pu(c, this.options, y, this.speed);
        this.updateMotionValue && this.updateMotionValue(v), hg(u, o, v), this.animation.cancel();
      }
      g?.(), this.notifyFinished();
    };
  }
  play() {
    this.isStopped || (this.manualStartTime = null, this.animation.play(), this.state === "finished" && this.updateFinished());
  }
  pause() {
    this.animation.pause();
  }
  complete() {
    this.animation.finish?.();
  }
  cancel() {
    try {
      this.animation.cancel();
    } catch {
    }
  }
  stop() {
    if (this.isStopped)
      return;
    this.isStopped = !0;
    const { state: l } = this;
    l === "idle" || l === "finished" || (this.updateMotionValue ? this.updateMotionValue() : this.commitStyles(), this.isPseudoElement || this.cancel());
  }
  /**
   * WAAPI doesn't natively have any interruption capabilities.
   *
   * In this method, we commit styles back to the DOM before cancelling
   * the animation.
   *
   * This is designed to be overridden by NativeAnimationExtended, which
   * will create a renderless JS animation and sample it twice to calculate
   * its current value, "previous" value, and therefore allow
   * Motion to also correctly calculate velocity for any subsequent animation
   * while deferring the commit until the next animation frame.
   */
  commitStyles() {
    const l = this.options?.element;
    !this.isPseudoElement && l?.isConnected && this.animation.commitStyles?.();
  }
  get duration() {
    const l = this.animation.effect?.getComputedTiming?.().duration || 0;
    return /* @__PURE__ */ Le(Number(l));
  }
  get iterationDuration() {
    const { delay: l = 0 } = this.options || {};
    return this.duration + /* @__PURE__ */ Le(l);
  }
  get time() {
    return /* @__PURE__ */ Le(Number(this.animation.currentTime) || 0);
  }
  set time(l) {
    const u = this.finishedTime !== null;
    this.manualStartTime = null, this.finishedTime = null, this.animation.currentTime = /* @__PURE__ */ Ce(l), u && this.animation.pause();
  }
  /**
   * The playback speed of the animation.
   * 1 = normal speed, 2 = double speed, 0.5 = half speed.
   */
  get speed() {
    return this.animation.playbackRate;
  }
  set speed(l) {
    l < 0 && (this.finishedTime = null), this.animation.playbackRate = l;
  }
  get state() {
    return this.finishedTime !== null ? "finished" : this.animation.playState;
  }
  get startTime() {
    return this.manualStartTime ?? Number(this.animation.startTime);
  }
  set startTime(l) {
    this.manualStartTime = this.animation.startTime = l;
  }
  /**
   * Attaches a timeline to the animation, for instance the `ScrollTimeline`.
   */
  attachTimeline({ timeline: l, rangeStart: u, rangeEnd: o, observe: c }) {
    return this.allowFlatten && this.animation.effect?.updateTiming({ easing: "linear" }), this.animation.onfinish = null, l && TT() ? (this.animation.timeline = l, u && (this.animation.rangeStart = u), o && (this.animation.rangeEnd = o), He) : c(this);
  }
}
const vg = {
  anticipate: Jp,
  backInOut: Kp,
  circInOut: Fp
};
function ET(i) {
  return i in vg;
}
function xT(i) {
  typeof i.ease == "string" && ET(i.ease) && (i.ease = vg[i.ease]);
}
const Wr = 10;
class MT extends gg {
  constructor(l) {
    xT(l), rg(l), super(l), l.startTime !== void 0 && l.autoplay !== !1 && (this.startTime = l.startTime), this.options = l;
  }
  /**
   * WAAPI doesn't natively have any interruption capabilities.
   *
   * Rather than read committed styles back out of the DOM, we can
   * create a renderless JS animation and sample it twice to calculate
   * its current value, "previous" value, and therefore allow
   * Motion to calculate velocity for any subsequent animation.
   */
  updateMotionValue(l) {
    const { motionValue: u, onUpdate: o, onComplete: c, element: d, ...h } = this.options;
    if (!u)
      return;
    if (l !== void 0) {
      u.set(l);
      return;
    }
    const y = new uu({
      ...h,
      autoplay: !1
    }), g = Math.max(Wr, oe.now() - this.startTime), m = Ie(0, Wr, g - Wr), v = y.sample(g).value, { name: S } = this.options;
    d && S && hg(d, S, v), u.setWithVelocity(y.sample(Math.max(0, g - m)).value, v, m), y.stop();
  }
}
const Vy = (i, l) => l === "zIndex" ? !1 : !!(typeof i == "number" || Array.isArray(i) || typeof i == "string" && // It's animatable if we have a string
(Qe.test(i) || i === "0") && // And it contains numbers and/or colors
!i.startsWith("url("));
function DT(i) {
  const l = i[0];
  if (i.length === 1)
    return !0;
  for (let u = 0; u < i.length; u++)
    if (i[u] !== l)
      return !0;
}
function CT(i, l, u, o) {
  const c = i[0];
  if (c === null)
    return !1;
  if (l === "display" || l === "visibility")
    return !0;
  const d = i[i.length - 1], h = Vy(c, l), y = Vy(d, l);
  return !h || !y ? !1 : DT(i) || (u === "spring" || pg(u)) && o;
}
function vc(i) {
  i.duration = 0, i.type = "keyframes";
}
const Sg = /* @__PURE__ */ new Set([
  "opacity",
  "clipPath",
  "filter",
  "transform",
  "backgroundColor"
]), zT = /^(?:oklch|oklab|lab|lch|color|color-mix|light-dark)\(/;
function RT(i) {
  for (let l = 0; l < i.length; l++)
    if (typeof i[l] == "string" && zT.test(i[l]))
      return !0;
  return !1;
}
const OT = /* @__PURE__ */ new Set([
  "color",
  "backgroundColor",
  "outlineColor",
  "fill",
  "stroke",
  "borderColor",
  "borderTopColor",
  "borderRightColor",
  "borderBottomColor",
  "borderLeftColor"
]), VT = /* @__PURE__ */ Yp(() => Object.hasOwnProperty.call(Element.prototype, "animate"));
function _T(i) {
  const { motionValue: l, name: u, repeatDelay: o, repeatType: c, damping: d, type: h, keyframes: y } = i, g = l?.owner?.current;
  if (!(g instanceof HTMLElement) && !(g instanceof SVGElement))
    return !1;
  const { onUpdate: m, transformTemplate: v } = l.owner.getProps();
  return VT() && u && /**
   * Force WAAPI for color properties with browser-only color formats
   * (oklch, oklab, lab, lch, etc.) that the JS animation path can't parse.
   */
  (Sg.has(u) || OT.has(u) && RT(y)) && (u !== "transform" || !v) && /**
   * If we're outputting values to onUpdate then we can't use WAAPI as there's
   * no way to read the value from WAAPI every frame.
   */
  !m && !o && c !== "mirror" && d !== 0 && h !== "inertia";
}
const UT = 40;
class BT extends Zc {
  constructor({ autoplay: l = !0, delay: u = 0, type: o = "keyframes", repeat: c = 0, repeatDelay: d = 0, repeatType: h = "loop", keyframes: y, name: g, motionValue: m, element: v, ...S }) {
    super(), this.stop = () => {
      this._animation && (this._animation.stop(), this.stopTimeline?.()), this.keyframeResolver?.cancel();
    }, this.createdAt = oe.now();
    const b = {
      autoplay: l,
      delay: u,
      type: o,
      repeat: c,
      repeatDelay: d,
      repeatType: h,
      name: g,
      motionValue: m,
      element: v,
      ...S
    }, _ = v?.KeyframeResolver || Qc;
    this.keyframeResolver = new _(y, (z, j, w) => this.onKeyframesResolved(z, j, b, !w), g, m, v), this.keyframeResolver?.scheduleResolve();
  }
  onKeyframesResolved(l, u, o, c) {
    this.keyframeResolver = void 0;
    const { name: d, type: h, velocity: y, delay: g, isHandoff: m, onUpdate: v } = o;
    this.resolvedAt = oe.now();
    let S = !0;
    CT(l, d, h, y) || (S = !1, (Kn.instantAnimations || !g) && v?.(pu(l, o, u)), l[0] = l[l.length - 1], vc(o), o.repeat = 0);
    const _ = {
      startTime: c ? this.resolvedAt ? this.resolvedAt - this.createdAt > UT ? this.resolvedAt : this.createdAt : this.createdAt : void 0,
      finalKeyframe: u,
      ...o,
      keyframes: l
    }, z = S && !m && _T(_), j = _.motionValue?.owner?.current;
    let w;
    if (z)
      try {
        w = new MT({
          ..._,
          element: j
        });
      } catch {
        w = new uu(_);
      }
    else
      w = new uu(_);
    w.finished.then(() => {
      this.notifyFinished();
    }).catch(He), this.pendingTimeline && (this.stopTimeline = w.attachTimeline(this.pendingTimeline), this.pendingTimeline = void 0), this._animation = w;
  }
  get finished() {
    return this._animation ? this.animation.finished : this._finished;
  }
  then(l, u) {
    return this.finished.finally(l).then(() => {
    });
  }
  get animation() {
    return this._animation || (this.keyframeResolver?.resume(), gT()), this._animation;
  }
  get duration() {
    return this.animation.duration;
  }
  get iterationDuration() {
    return this.animation.iterationDuration;
  }
  get time() {
    return this.animation.time;
  }
  set time(l) {
    this.animation.time = l;
  }
  get speed() {
    return this.animation.speed;
  }
  get state() {
    return this.animation.state;
  }
  set speed(l) {
    this.animation.speed = l;
  }
  get startTime() {
    return this.animation.startTime;
  }
  attachTimeline(l) {
    return this._animation ? this.stopTimeline = this.animation.attachTimeline(l) : this.pendingTimeline = l, () => this.stop();
  }
  play() {
    this.animation.play();
  }
  pause() {
    this.animation.pause();
  }
  complete() {
    this.animation.complete();
  }
  cancel() {
    this._animation && this.animation.cancel(), this.keyframeResolver?.cancel();
  }
}
function Tg(i, l, u, o = 0, c = 1) {
  const d = Array.from(i).sort((m, v) => m.sortNodePosition(v)).indexOf(l), h = i.size, y = (h - 1) * o;
  return typeof u == "function" ? u(d, h) : c === 1 ? d * o : y - d * o;
}
const _y = 30, NT = (i) => !isNaN(parseFloat(i));
class jT {
  /**
   * @param init - The initiating value
   * @param config - Optional configuration options
   *
   * -  `transformer`: A function to transform incoming values with.
   */
  constructor(l, u = {}) {
    this.canTrackVelocity = null, this.events = {}, this.updateAndNotify = (o) => {
      const c = oe.now();
      if (this.updatedAt !== c && this.setPrevFrameValue(), this.prev = this.current, this.setCurrent(o), this.current !== this.prev && (this.events.change?.notify(this.current), this.dependents))
        for (const d of this.dependents)
          d.dirty();
    }, this.hasAnimated = !1, this.setCurrent(l), this.owner = u.owner;
  }
  setCurrent(l) {
    this.current = l, this.updatedAt = oe.now(), this.canTrackVelocity === null && l !== void 0 && (this.canTrackVelocity = NT(this.current));
  }
  setPrevFrameValue(l = this.current) {
    this.prevFrameValue = l, this.prevUpdatedAt = this.updatedAt;
  }
  /**
   * Adds a function that will be notified when the `MotionValue` is updated.
   *
   * It returns a function that, when called, will cancel the subscription.
   *
   * When calling `onChange` inside a React component, it should be wrapped with the
   * `useEffect` hook. As it returns an unsubscribe function, this should be returned
   * from the `useEffect` function to ensure you don't add duplicate subscribers..
   *
   * ```jsx
   * export const MyComponent = () => {
   *   const x = useMotionValue(0)
   *   const y = useMotionValue(0)
   *   const opacity = useMotionValue(1)
   *
   *   useEffect(() => {
   *     function updateOpacity() {
   *       const maxXY = Math.max(x.get(), y.get())
   *       const newOpacity = transform(maxXY, [0, 100], [1, 0])
   *       opacity.set(newOpacity)
   *     }
   *
   *     const unsubscribeX = x.on("change", updateOpacity)
   *     const unsubscribeY = y.on("change", updateOpacity)
   *
   *     return () => {
   *       unsubscribeX()
   *       unsubscribeY()
   *     }
   *   }, [])
   *
   *   return <motion.div style={{ x }} />
   * }
   * ```
   *
   * @param subscriber - A function that receives the latest value.
   * @returns A function that, when called, will cancel this subscription.
   *
   * @deprecated
   */
  onChange(l) {
    return this.on("change", l);
  }
  on(l, u) {
    this.events[l] || (this.events[l] = new jc());
    const o = this.events[l].add(u);
    return l === "change" ? () => {
      o(), Ot.read(() => {
        this.events.change.getSize() || this.stop();
      });
    } : o;
  }
  clearListeners() {
    for (const l in this.events)
      this.events[l].clear();
  }
  /**
   * Attaches a passive effect to the `MotionValue`.
   */
  attach(l, u) {
    this.passiveEffect = l, this.stopPassiveEffect = u;
  }
  /**
   * Sets the state of the `MotionValue`.
   *
   * @remarks
   *
   * ```jsx
   * const x = useMotionValue(0)
   * x.set(10)
   * ```
   *
   * @param latest - Latest value to set.
   * @param render - Whether to notify render subscribers. Defaults to `true`
   *
   * @public
   */
  set(l) {
    this.passiveEffect ? this.passiveEffect(l, this.updateAndNotify) : this.updateAndNotify(l);
  }
  setWithVelocity(l, u, o) {
    this.set(u), this.prev = void 0, this.prevFrameValue = l, this.prevUpdatedAt = this.updatedAt - o;
  }
  /**
   * Set the state of the `MotionValue`, stopping any active animations,
   * effects, and resets velocity to `0`.
   */
  jump(l, u = !0) {
    this.updateAndNotify(l), this.prev = l, this.prevUpdatedAt = this.prevFrameValue = void 0, u && this.stop(), this.stopPassiveEffect && this.stopPassiveEffect();
  }
  dirty() {
    this.events.change?.notify(this.current);
  }
  addDependent(l) {
    this.dependents || (this.dependents = /* @__PURE__ */ new Set()), this.dependents.add(l);
  }
  removeDependent(l) {
    this.dependents && this.dependents.delete(l);
  }
  /**
   * Returns the latest state of `MotionValue`
   *
   * @returns - The latest state of `MotionValue`
   *
   * @public
   */
  get() {
    return this.current;
  }
  /**
   * @public
   */
  getPrevious() {
    return this.prev;
  }
  /**
   * Returns the latest velocity of `MotionValue`
   *
   * @returns - The latest velocity of `MotionValue`. Returns `0` if the state is non-numerical.
   *
   * @public
   */
  getVelocity() {
    const l = oe.now();
    if (!this.canTrackVelocity || this.prevFrameValue === void 0 || l - this.updatedAt > _y)
      return 0;
    const u = Math.min(this.updatedAt - this.prevUpdatedAt, _y);
    return /* @__PURE__ */ qp(parseFloat(this.current) - parseFloat(this.prevFrameValue), u);
  }
  /**
   * Registers a new animation to control this `MotionValue`. Only one
   * animation can drive a `MotionValue` at one time.
   *
   * ```jsx
   * value.start()
   * ```
   *
   * @param animation - A function that starts the provided animation
   */
  start(l) {
    return this.stop(), new Promise((u) => {
      this.hasAnimated = !0, this.animation = l(u), this.events.animationStart && this.events.animationStart.notify();
    }).then(() => {
      this.events.animationComplete && this.events.animationComplete.notify(), this.clearAnimation();
    });
  }
  /**
   * Stop the currently active animation.
   *
   * @public
   */
  stop() {
    this.animation && (this.animation.stop(), this.events.animationCancel && this.events.animationCancel.notify()), this.clearAnimation();
  }
  /**
   * Returns `true` if this value is currently animating.
   *
   * @public
   */
  isAnimating() {
    return !!this.animation;
  }
  clearAnimation() {
    delete this.animation;
  }
  /**
   * Destroy and clean up subscribers to this `MotionValue`.
   *
   * The `MotionValue` hooks like `useMotionValue` and `useTransform` automatically
   * handle the lifecycle of the returned `MotionValue`, so this method is only necessary if you've manually
   * created a `MotionValue` via the `motionValue` function.
   *
   * @public
   */
  destroy() {
    this.dependents?.clear(), this.events.destroy?.notify(), this.clearListeners(), this.stop(), this.stopPassiveEffect && this.stopPassiveEffect();
  }
}
function ra(i, l) {
  return new jT(i, l);
}
function Kc(i, l) {
  if (i?.inherit && l) {
    const { inherit: u, ...o } = i;
    return { ...l, ...o };
  }
  return i;
}
function Jc(i, l) {
  const u = i?.[l] ?? i?.default ?? i;
  return u !== i ? Kc(u, i) : u;
}
const wT = {
  type: "spring",
  stiffness: 500,
  damping: 25,
  restSpeed: 10
}, LT = (i) => ({
  type: "spring",
  stiffness: 550,
  damping: i === 0 ? 2 * Math.sqrt(550) : 30,
  restSpeed: 10
}), HT = {
  type: "keyframes",
  duration: 0.8
}, YT = {
  type: "keyframes",
  ease: [0.25, 0.1, 0.35, 1],
  duration: 0.3
}, qT = (i, { keyframes: l }) => l.length > 2 ? HT : ha.has(i) ? i.startsWith("scale") ? LT(l[1]) : wT : YT, GT = /* @__PURE__ */ new Set([
  "when",
  "delay",
  "delayChildren",
  "staggerChildren",
  "staggerDirection",
  "repeat",
  "repeatType",
  "repeatDelay",
  "from",
  "elapsed"
]);
function XT(i) {
  for (const l in i)
    if (!GT.has(l))
      return !0;
  return !1;
}
const kc = (i, l, u, o = {}, c, d) => (h) => {
  const y = Jc(o, i) || {}, g = y.delay || o.delay || 0;
  let { elapsed: m = 0 } = o;
  m = m - /* @__PURE__ */ Ce(g);
  const v = {
    keyframes: Array.isArray(u) ? u : [null, u],
    ease: "easeOut",
    velocity: l.getVelocity(),
    ...y,
    delay: -m,
    onUpdate: (b) => {
      l.set(b), y.onUpdate && y.onUpdate(b);
    },
    onComplete: () => {
      h(), y.onComplete && y.onComplete();
    },
    name: i,
    motionValue: l,
    element: d ? void 0 : c
  };
  XT(y) || Object.assign(v, qT(i, v)), v.duration && (v.duration = /* @__PURE__ */ Ce(v.duration)), v.repeatDelay && (v.repeatDelay = /* @__PURE__ */ Ce(v.repeatDelay)), v.from !== void 0 && (v.keyframes[0] = v.from);
  let S = !1;
  if ((v.type === !1 || v.duration === 0 && !v.repeatDelay) && (vc(v), v.delay === 0 && (S = !0)), (Kn.instantAnimations || Kn.skipAnimations || c?.shouldSkipAnimations || y.skipAnimations) && (S = !0, vc(v), v.delay = 0), v.allowFlatten = !y.type && !y.ease, S && !d && l.get() !== void 0) {
    const b = pu(v.keyframes, y);
    if (b !== void 0) {
      Ot.update(() => {
        v.onUpdate(b), v.onComplete();
      });
      return;
    }
  }
  return y.isSync ? new uu(v) : new BT(v);
}, ZT = (
  // eslint-disable-next-line redos-detector/no-unsafe-regex -- false positive, as it can match a lot of words
  /^var\(--(?:([\w-]+)|([\w-]+), ?([a-zA-Z\d ()%#.,-]+))\)/u
);
function QT(i) {
  const l = ZT.exec(i);
  if (!l)
    return [,];
  const [, u, o, c] = l;
  return [`--${u ?? o}`, c];
}
function bg(i, l, u = 1) {
  const [o, c] = QT(i);
  if (!o)
    return;
  const d = window.getComputedStyle(l).getPropertyValue(o);
  if (d) {
    const h = d.trim();
    return wp(h) ? parseFloat(h) : h;
  }
  return Hc(c) ? bg(c, l, u + 1) : c;
}
function Uy(i) {
  const l = [{}, {}];
  return i?.values.forEach((u, o) => {
    l[0][o] = u.get(), l[1][o] = u.getVelocity();
  }), l;
}
function Fc(i, l, u, o) {
  if (typeof l == "function") {
    const [c, d] = Uy(o);
    l = l(u !== void 0 ? u : i.custom, c, d);
  }
  if (typeof l == "string" && (l = i.variants && i.variants[l]), typeof l == "function") {
    const [c, d] = Uy(o);
    l = l(u !== void 0 ? u : i.custom, c, d);
  }
  return l;
}
function Si(i, l, u) {
  const o = i.getProps();
  return Fc(o, l, u !== void 0 ? u : o.custom, i);
}
const Ag = /* @__PURE__ */ new Set([
  "width",
  "height",
  "top",
  "left",
  "right",
  "bottom",
  ...fa
]), Sc = (i) => Array.isArray(i);
function KT(i, l, u) {
  i.hasValue(l) ? i.getValue(l).set(u) : i.addValue(l, ra(u));
}
function JT(i) {
  return Sc(i) ? i[i.length - 1] || 0 : i;
}
function kT(i, l) {
  const u = Si(i, l);
  let { transitionEnd: o = {}, transition: c = {}, ...d } = u || {};
  d = { ...d, ...o };
  for (const h in d) {
    const y = JT(d[h]);
    KT(i, h, y);
  }
}
const ae = (i) => !!(i && i.getVelocity);
function FT(i) {
  return !!(ae(i) && i.add);
}
function Tc(i, l) {
  const u = i.getValue("willChange");
  if (FT(u))
    return u.add(l);
  if (!u && Kn.WillChange) {
    const o = new Kn.WillChange("auto");
    i.addValue("willChange", o), o.add(l);
  }
}
function Wc(i) {
  return i.replace(/([A-Z])/g, (l) => `-${l.toLowerCase()}`);
}
const WT = "framerAppearId", Eg = "data-" + Wc(WT);
function xg(i) {
  return i.props[Eg];
}
function PT({ protectedKeys: i, needsAnimating: l }, u) {
  const o = i.hasOwnProperty(u) && l[u] !== !0;
  return l[u] = !1, o;
}
function Mg(i, l, { delay: u = 0, transitionOverride: o, type: c } = {}) {
  let { transition: d, transitionEnd: h, ...y } = l;
  const g = i.getDefaultTransition();
  d = d ? Kc(d, g) : g;
  const m = d?.reduceMotion, v = d?.skipAnimations;
  o && (d = o);
  const S = [], b = c && i.animationState && i.animationState.getState()[c], _ = d?.path;
  _ && _.animateVisualElement(i, y, d, u, S);
  for (const z in y) {
    const j = i.getValue(z, i.latestValues[z] ?? null), w = y[z];
    if (w === void 0 || b && PT(b, z))
      continue;
    const L = {
      delay: u,
      ...Jc(d || {}, z)
    };
    v && (L.skipAnimations = !0);
    const G = j.get();
    if (G !== void 0 && !j.isAnimating() && !Array.isArray(w) && w === G && !L.velocity) {
      Ot.update(() => j.set(w));
      continue;
    }
    let H = !1;
    if (window.MotionHandoffAnimation) {
      const nt = xg(i);
      if (nt) {
        const Q = window.MotionHandoffAnimation(nt, z, Ot);
        Q !== null && (L.startTime = Q, H = !0);
      }
    }
    Tc(i, z);
    const Y = m ?? i.shouldReduceMotion;
    j.start(kc(z, j, w, Y && Ag.has(z) ? { type: !1 } : L, i, H));
    const tt = j.animation;
    tt && S.push(tt);
  }
  if (h) {
    const z = () => Ot.update(() => {
      h && kT(i, h);
    });
    S.length ? Promise.all(S).then(z) : z();
  }
  return S;
}
function bc(i, l, u = {}) {
  const o = Si(i, l, u.type === "exit" ? i.presenceContext?.custom : void 0);
  let { transition: c = i.getDefaultTransition() || {} } = o || {};
  u.transitionOverride && (c = u.transitionOverride);
  const d = o ? () => Promise.all(Mg(i, o, u)) : () => Promise.resolve(), h = i.variantChildren && i.variantChildren.size ? (g = 0) => {
    const { delayChildren: m = 0, staggerChildren: v, staggerDirection: S } = c;
    return $T(i, l, g, m, v, S, u);
  } : () => Promise.resolve(), { when: y } = c;
  if (y) {
    const [g, m] = y === "beforeChildren" ? [d, h] : [h, d];
    return g().then(() => m());
  } else
    return Promise.all([d(), h(u.delay)]);
}
function $T(i, l, u = 0, o = 0, c = 0, d = 1, h) {
  const y = [];
  for (const g of i.variantChildren)
    g.notify("AnimationStart", l), y.push(bc(g, l, {
      ...h,
      delay: u + (typeof o == "function" ? 0 : o) + Tg(i.variantChildren, g, o, c, d)
    }).then(() => g.notify("AnimationComplete", l)));
  return Promise.all(y);
}
function IT(i, l, u = {}) {
  i.notify("AnimationStart", l);
  let o;
  if (Array.isArray(l)) {
    const c = l.map((d) => bc(i, d, u));
    o = Promise.all(c);
  } else if (typeof l == "string")
    o = bc(i, l, u);
  else {
    const c = typeof l == "function" ? Si(i, l, u.custom) : l;
    o = Promise.all(Mg(i, c, u));
  }
  return o.then(() => {
    i.notify("AnimationComplete", l);
  });
}
const tb = {
  test: (i) => i === "auto",
  parse: (i) => i
}, Dg = (i) => (l) => l.test(i), Cg = [ca, F, $e, Sn, DS, MS, tb], By = (i) => Cg.find(Dg(i));
function eb(i) {
  return typeof i == "number" ? i === 0 : i !== null ? i === "none" || i === "0" || Hp(i) : !0;
}
const nb = /* @__PURE__ */ new Set(["brightness", "contrast", "saturate", "opacity"]);
function ib(i) {
  const [l, u] = i.slice(0, -1).split("(");
  if (l === "drop-shadow")
    return i;
  const [o] = u.match(Yc) || [];
  if (!o)
    return i;
  const c = u.replace(o, "");
  let d = nb.has(l) ? 1 : 0;
  return o !== u && (d *= 100), l + "(" + d + c + ")";
}
const ab = /\b([a-z-]*)\(.*?\)/gu, Ac = {
  ...Qe,
  getAnimatableNone: (i) => {
    const l = i.match(ab);
    return l ? l.map(ib).join(" ") : i;
  }
}, Ec = {
  ...Qe,
  getAnimatableNone: (i) => {
    const l = Qe.parse(i);
    return Qe.createTransformer(i)(l.map((o) => typeof o == "number" ? 0 : typeof o == "object" ? { ...o, alpha: 1 } : o));
  }
}, Ny = {
  ...ca,
  transform: Math.round
}, lb = {
  rotate: Sn,
  /**
   * Internal channel for `transition.path` orientToPath. Composed onto
   * `rotate` at the transform-build sites so the user's `rotate` is
   * never read or overwritten. Not part of `transformPropOrder`.
   */
  pathRotation: Sn,
  rotateX: Sn,
  rotateY: Sn,
  rotateZ: Sn,
  scale: Xs,
  scaleX: Xs,
  scaleY: Xs,
  scaleZ: Xs,
  skew: Sn,
  skewX: Sn,
  skewY: Sn,
  distance: F,
  translateX: F,
  translateY: F,
  translateZ: F,
  x: F,
  y: F,
  z: F,
  perspective: F,
  transformPerspective: F,
  opacity: yl,
  originX: by,
  originY: by,
  originZ: F
}, ou = {
  // Border props
  borderWidth: F,
  borderTopWidth: F,
  borderRightWidth: F,
  borderBottomWidth: F,
  borderLeftWidth: F,
  borderRadius: F,
  borderTopLeftRadius: F,
  borderTopRightRadius: F,
  borderBottomRightRadius: F,
  borderBottomLeftRadius: F,
  // Positioning props
  width: F,
  maxWidth: F,
  height: F,
  maxHeight: F,
  top: F,
  right: F,
  bottom: F,
  left: F,
  inset: F,
  insetBlock: F,
  insetBlockStart: F,
  insetBlockEnd: F,
  insetInline: F,
  insetInlineStart: F,
  insetInlineEnd: F,
  // Spacing props
  padding: F,
  paddingTop: F,
  paddingRight: F,
  paddingBottom: F,
  paddingLeft: F,
  paddingBlock: F,
  paddingBlockStart: F,
  paddingBlockEnd: F,
  paddingInline: F,
  paddingInlineStart: F,
  paddingInlineEnd: F,
  margin: F,
  marginTop: F,
  marginRight: F,
  marginBottom: F,
  marginLeft: F,
  marginBlock: F,
  marginBlockStart: F,
  marginBlockEnd: F,
  marginInline: F,
  marginInlineStart: F,
  marginInlineEnd: F,
  // Typography
  fontSize: F,
  // Misc
  backgroundPositionX: F,
  backgroundPositionY: F,
  ...lb,
  zIndex: Ny,
  // SVG
  fillOpacity: yl,
  strokeOpacity: yl,
  numOctaves: Ny
}, sb = {
  ...ou,
  // Color props
  color: Kt,
  backgroundColor: Kt,
  outlineColor: Kt,
  fill: Kt,
  stroke: Kt,
  // Border props
  borderColor: Kt,
  borderTopColor: Kt,
  borderRightColor: Kt,
  borderBottomColor: Kt,
  borderLeftColor: Kt,
  filter: Ac,
  WebkitFilter: Ac,
  mask: Ec,
  WebkitMask: Ec
}, zg = (i) => sb[i], ub = /* @__PURE__ */ new Set([Ac, Ec]);
function Rg(i, l) {
  let u = zg(i);
  return ub.has(u) || (u = Qe), u.getAnimatableNone ? u.getAnimatableNone(l) : void 0;
}
const ob = /* @__PURE__ */ new Set(["auto", "none", "0"]);
function rb(i, l, u) {
  let o = 0, c;
  for (; o < i.length && !c; ) {
    const d = i[o];
    typeof d == "string" && !ob.has(d) && oa(d).values.length && (c = i[o]), o++;
  }
  if (c && u)
    for (const d of l)
      i[d] = Rg(u, c);
}
class cb extends Qc {
  constructor(l, u, o, c, d) {
    super(l, u, o, c, d, !0);
  }
  readKeyframes() {
    const { unresolvedKeyframes: l, element: u, name: o } = this;
    if (!u || !u.current)
      return;
    super.readKeyframes();
    for (let v = 0; v < l.length; v++) {
      let S = l[v];
      if (typeof S == "string" && (S = S.trim(), Hc(S))) {
        const b = bg(S, u.current);
        b !== void 0 && (l[v] = b), v === l.length - 1 && (this.finalKeyframe = S);
      }
    }
    if (this.resolveNoneKeyframes(), !Ag.has(o) || l.length !== 2)
      return;
    const [c, d] = l, h = By(c), y = By(d), g = Ty(c), m = Ty(d);
    if (g !== m && Qn[o]) {
      this.needsMeasurement = !0;
      return;
    }
    if (h !== y)
      if (Ry(h) && Ry(y))
        for (let v = 0; v < l.length; v++) {
          const S = l[v];
          typeof S == "string" && (l[v] = parseFloat(S));
        }
      else Qn[o] && (this.needsMeasurement = !0);
  }
  resolveNoneKeyframes() {
    const { unresolvedKeyframes: l, name: u } = this, o = [];
    for (let c = 0; c < l.length; c++)
      (l[c] === null || eb(l[c])) && o.push(c);
    o.length && rb(l, o, u);
  }
  measureInitialState() {
    const { element: l, unresolvedKeyframes: u, name: o } = this;
    if (!l || !l.current)
      return;
    o === "height" && (this.suspendedScrollY = window.pageYOffset), this.measuredOrigin = Qn[o](l.measureViewportBox(), window.getComputedStyle(l.current)), u[0] = this.measuredOrigin;
    const c = u[u.length - 1];
    c !== void 0 && l.getValue(o, c).jump(c, !1);
  }
  measureEndState() {
    const { element: l, name: u, unresolvedKeyframes: o } = this;
    if (!l || !l.current)
      return;
    const c = l.getValue(u);
    c && c.jump(this.measuredOrigin, !1);
    const d = o.length - 1, h = o[d];
    o[d] = Qn[u](l.measureViewportBox(), window.getComputedStyle(l.current)), h !== null && this.finalKeyframe === void 0 && (this.finalKeyframe = h), this.removedTransforms?.length && this.removedTransforms.forEach(([y, g]) => {
      l.getValue(y).set(g);
    }), this.resolveNoneKeyframes();
  }
}
const Pc = [
  "borderTopLeftRadius",
  "borderTopRightRadius",
  "borderBottomRightRadius",
  "borderBottomLeftRadius"
];
function Og(i, l, u) {
  if (i == null)
    return [];
  if (i instanceof EventTarget)
    return [i];
  if (typeof i == "string") {
    let o = document;
    const c = u?.[i] ?? o.querySelectorAll(i);
    return c ? Array.from(c) : [];
  }
  return Array.from(i).filter((o) => o != null);
}
const xc = (i, l) => l && typeof i == "number" ? l.transform(i) : i;
function Fs(i) {
  return Lp(i) && "offsetHeight" in i && !("ownerSVGElement" in i);
}
const { schedule: $c } = /* @__PURE__ */ $p(queueMicrotask, !1), Ze = {
  x: !1,
  y: !1
};
function Vg() {
  return Ze.x || Ze.y;
}
function fb(i) {
  return i === "x" || i === "y" ? Ze[i] ? null : (Ze[i] = !0, () => {
    Ze[i] = !1;
  }) : Ze.x || Ze.y ? null : (Ze.x = Ze.y = !0, () => {
    Ze.x = Ze.y = !1;
  });
}
function _g(i, l) {
  const u = Og(i), o = new AbortController(), c = {
    passive: !0,
    ...l,
    signal: o.signal
  };
  return [u, c, () => o.abort()];
}
function hb(i) {
  return !(i.pointerType === "touch" || Vg());
}
function db(i, l, u = {}) {
  const [o, c, d] = _g(i, u);
  return o.forEach((h) => {
    let y = !1, g = !1, m;
    const v = () => {
      h.removeEventListener("pointerleave", z);
    }, S = (w) => {
      m && (m(w), m = void 0), v();
    }, b = (w) => {
      y = !1, window.removeEventListener("pointerup", b), window.removeEventListener("pointercancel", b), g && (g = !1, S(w));
    }, _ = () => {
      y = !0, window.addEventListener("pointerup", b, c), window.addEventListener("pointercancel", b, c);
    }, z = (w) => {
      if (w.pointerType !== "touch") {
        if (y) {
          g = !0;
          return;
        }
        S(w);
      }
    }, j = (w) => {
      if (!hb(w))
        return;
      g = !1;
      const L = l(h, w);
      typeof L == "function" && (m = L, h.addEventListener("pointerleave", z, c));
    };
    h.addEventListener("pointerenter", j, c), h.addEventListener("pointerdown", _, c);
  }), d;
}
const Ug = (i, l) => l ? i === l ? !0 : Ug(i, l.parentElement) : !1, Ic = (i) => i.pointerType === "mouse" ? typeof i.button != "number" || i.button <= 0 : i.isPrimary !== !1, mb = /* @__PURE__ */ new Set([
  "BUTTON",
  "INPUT",
  "SELECT",
  "TEXTAREA",
  "A"
]);
function yb(i) {
  return mb.has(i.tagName) || i.isContentEditable === !0;
}
const pb = /* @__PURE__ */ new Set(["INPUT", "SELECT", "TEXTAREA"]);
function gb(i) {
  return pb.has(i.tagName) || i.isContentEditable === !0;
}
const Ws = /* @__PURE__ */ new WeakSet();
function jy(i) {
  return (l) => {
    l.key === "Enter" && i(l);
  };
}
function Pr(i, l) {
  i.dispatchEvent(new PointerEvent("pointer" + l, { isPrimary: !0, bubbles: !0 }));
}
const vb = (i, l) => {
  const u = i.currentTarget;
  if (!u)
    return;
  const o = jy(() => {
    if (Ws.has(u))
      return;
    Pr(u, "down");
    const c = jy(() => {
      Pr(u, "up");
    }), d = () => Pr(u, "cancel");
    u.addEventListener("keyup", c, l), u.addEventListener("blur", d, l);
  });
  u.addEventListener("keydown", o, l), u.addEventListener("blur", () => u.removeEventListener("keydown", o), l);
};
function wy(i) {
  return Ic(i) && !Vg();
}
const Ly = /* @__PURE__ */ new WeakSet();
function Sb(i, l, u = {}) {
  const [o, c, d] = _g(i, u), h = (y) => {
    const g = y.currentTarget;
    if (!wy(y) || Ly.has(y))
      return;
    Ws.add(g), u.stopPropagation && Ly.add(y);
    const m = l(g, y), v = { ...c, capture: !0 }, S = (z, j) => {
      window.removeEventListener("pointerup", b, v), window.removeEventListener("pointercancel", _, v), Ws.has(g) && Ws.delete(g), wy(z) && typeof m == "function" && m(z, { success: j });
    }, b = (z) => {
      S(z, g === window || g === document || u.useGlobalTarget || Ug(g, z.target));
    }, _ = (z) => {
      S(z, !1);
    };
    window.addEventListener("pointerup", b, v), window.addEventListener("pointercancel", _, v);
  };
  return o.forEach((y) => {
    (u.useGlobalTarget ? window : y).addEventListener("pointerdown", h, c), Fs(y) && (y.addEventListener("focus", (m) => vb(m, c)), !yb(y) && !y.hasAttribute("tabindex") && (y.tabIndex = 0));
  }), d;
}
function tf(i) {
  return Lp(i) && "ownerSVGElement" in i;
}
const Ps = /* @__PURE__ */ new WeakMap();
let $s;
const Bg = (i, l, u) => (o, c) => c && c[0] ? c[0][i + "Size"] : tf(o) && "getBBox" in o ? o.getBBox()[l] : o[u], Tb = /* @__PURE__ */ Bg("inline", "width", "offsetWidth"), bb = /* @__PURE__ */ Bg("block", "height", "offsetHeight");
function Ab({ target: i, borderBoxSize: l }) {
  Ps.get(i)?.forEach((u) => {
    u(i, {
      get width() {
        return Tb(i, l);
      },
      get height() {
        return bb(i, l);
      }
    });
  });
}
function Eb(i) {
  i.forEach(Ab);
}
function xb() {
  typeof ResizeObserver > "u" || ($s = new ResizeObserver(Eb));
}
function Mb(i, l) {
  $s || xb();
  const u = Og(i);
  return u.forEach((o) => {
    let c = Ps.get(o);
    c || (c = /* @__PURE__ */ new Set(), Ps.set(o, c)), c.add(l), $s?.observe(o);
  }), () => {
    u.forEach((o) => {
      const c = Ps.get(o);
      c?.delete(l), c?.size || $s?.unobserve(o);
    });
  };
}
const Is = /* @__PURE__ */ new Set();
let sa;
function Db() {
  sa = () => {
    const i = {
      get width() {
        return window.innerWidth;
      },
      get height() {
        return window.innerHeight;
      }
    };
    Is.forEach((l) => l(i));
  }, window.addEventListener("resize", sa);
}
function Cb(i) {
  return Is.add(i), sa || Db(), () => {
    Is.delete(i), !Is.size && typeof sa == "function" && (window.removeEventListener("resize", sa), sa = void 0);
  };
}
function Hy(i, l) {
  return typeof i == "function" ? Cb(i) : Mb(i, l);
}
function zb(i) {
  return tf(i) && i.tagName === "svg";
}
const Rb = [...Cg, Kt, Qe], Ob = (i) => Rb.find(Dg(i)), Yy = () => ({
  translate: 0,
  scale: 1,
  origin: 0,
  originPoint: 0
}), ua = () => ({
  x: Yy(),
  y: Yy()
}), qy = () => ({ min: 0, max: 0 }), kt = () => ({
  x: qy(),
  y: qy()
}), Vb = /* @__PURE__ */ new WeakMap();
function gu(i) {
  return i !== null && typeof i == "object" && typeof i.start == "function";
}
function pl(i) {
  return typeof i == "string" || Array.isArray(i);
}
const ef = [
  "animate",
  "whileInView",
  "whileFocus",
  "whileHover",
  "whileTap",
  "whileDrag",
  "exit"
], nf = ["initial", ...ef];
function vu(i) {
  return gu(i.animate) || nf.some((l) => pl(i[l]));
}
function Ng(i) {
  return !!(vu(i) || i.variants);
}
function _b(i, l, u) {
  for (const o in l) {
    const c = l[o], d = u[o];
    if (ae(c))
      i.addValue(o, c);
    else if (ae(d))
      i.addValue(o, ra(c, { owner: i }));
    else if (d !== c)
      if (i.hasValue(o)) {
        const h = i.getValue(o);
        h.liveStyle === !0 ? h.jump(c) : h.hasAnimated || h.set(c);
      } else {
        const h = i.getStaticValue(o);
        i.addValue(o, ra(h !== void 0 ? h : c, { owner: i }));
      }
  }
  for (const o in u)
    l[o] === void 0 && i.removeValue(o);
  return l;
}
const Mc = { current: null }, jg = { current: !1 }, Ub = typeof window < "u";
function Bb() {
  if (jg.current = !0, !!Ub)
    if (window.matchMedia) {
      const i = window.matchMedia("(prefers-reduced-motion)"), l = () => Mc.current = i.matches;
      i.addEventListener("change", l), l();
    } else
      Mc.current = !1;
}
const Gy = [
  "AnimationStart",
  "AnimationComplete",
  "Update",
  "BeforeLayoutMeasure",
  "LayoutMeasure",
  "LayoutAnimationStart",
  "LayoutAnimationComplete"
];
let ru = {};
function wg(i) {
  ru = i;
}
function Nb() {
  return ru;
}
class jb {
  /**
   * This method takes React props and returns found MotionValues. For example, HTML
   * MotionValues will be found within the style prop, whereas for Three.js within attribute arrays.
   *
   * This isn't an abstract method as it needs calling in the constructor, but it is
   * intended to be one.
   */
  scrapeMotionValuesFromProps(l, u, o) {
    return {};
  }
  constructor({ parent: l, props: u, presenceContext: o, reducedMotionConfig: c, skipAnimations: d, blockInitialAnimation: h, visualState: y }, g = {}) {
    this.current = null, this.children = /* @__PURE__ */ new Set(), this.isVariantNode = !1, this.isControllingVariants = !1, this.shouldReduceMotion = null, this.shouldSkipAnimations = !1, this.values = /* @__PURE__ */ new Map(), this.KeyframeResolver = Qc, this.features = {}, this.valueSubscriptions = /* @__PURE__ */ new Map(), this.prevMotionValues = {}, this.hasBeenMounted = !1, this.events = {}, this.propEventSubscriptions = {}, this.notifyUpdate = () => this.notify("Update", this.latestValues), this.render = () => {
      this.current && (this.triggerBuild(), this.renderInstance(this.current, this.renderState, this.props.style, this.projection));
    }, this.renderScheduledAt = 0, this.scheduleRender = () => {
      const _ = oe.now();
      this.renderScheduledAt < _ && (this.renderScheduledAt = _, Ot.render(this.render, !1, !0));
    };
    const { latestValues: m, renderState: v } = y;
    this.latestValues = m, this.baseTarget = { ...m }, this.initialValues = u.initial ? { ...m } : {}, this.renderState = v, this.parent = l, this.props = u, this.presenceContext = o, this.depth = l ? l.depth + 1 : 0, this.reducedMotionConfig = c, this.skipAnimationsConfig = d, this.options = g, this.blockInitialAnimation = !!h, this.isControllingVariants = vu(u), this.isVariantNode = Ng(u), this.isVariantNode && (this.variantChildren = /* @__PURE__ */ new Set()), this.manuallyAnimateOnMount = !!(l && l.current);
    const { willChange: S, ...b } = this.scrapeMotionValuesFromProps(u, {}, this);
    for (const _ in b) {
      const z = b[_];
      m[_] !== void 0 && ae(z) && z.set(m[_]);
    }
  }
  mount(l) {
    if (this.hasBeenMounted)
      for (const u in this.initialValues)
        this.values.get(u)?.jump(this.initialValues[u]), this.latestValues[u] = this.initialValues[u];
    this.current = l, Vb.set(l, this), this.projection && !this.projection.instance && this.projection.mount(l), this.parent && this.isVariantNode && !this.isControllingVariants && (this.removeFromVariantTree = this.parent.addVariantChild(this)), this.values.forEach((u, o) => this.bindToMotionValue(o, u)), this.reducedMotionConfig === "never" ? this.shouldReduceMotion = !1 : this.reducedMotionConfig === "always" ? this.shouldReduceMotion = !0 : (jg.current || Bb(), this.shouldReduceMotion = Mc.current), this.shouldSkipAnimations = this.skipAnimationsConfig ?? !1, this.parent?.addChild(this), this.update(this.props, this.presenceContext), this.hasBeenMounted = !0;
  }
  unmount() {
    this.projection && this.projection.unmount(), Jn(this.notifyUpdate), Jn(this.render), this.valueSubscriptions.forEach((l) => l()), this.valueSubscriptions.clear(), this.removeFromVariantTree && this.removeFromVariantTree(), this.parent?.removeChild(this);
    for (const l in this.events)
      this.events[l].clear();
    for (const l in this.features) {
      const u = this.features[l];
      u && (u.unmount(), u.isMounted = !1);
    }
    this.current = null;
  }
  addChild(l) {
    this.children.add(l), this.enteringChildren ?? (this.enteringChildren = /* @__PURE__ */ new Set()), this.enteringChildren.add(l);
  }
  removeChild(l) {
    this.children.delete(l), this.enteringChildren && this.enteringChildren.delete(l);
  }
  bindToMotionValue(l, u) {
    if (this.valueSubscriptions.has(l) && this.valueSubscriptions.get(l)(), u.accelerate && Sg.has(l) && this.current instanceof HTMLElement) {
      const { factory: h, keyframes: y, times: g, ease: m, duration: v } = u.accelerate, S = new gg({
        element: this.current,
        name: l,
        keyframes: y,
        times: g,
        ease: m,
        duration: /* @__PURE__ */ Ce(v)
      }), b = h(S);
      this.valueSubscriptions.set(l, () => {
        b(), S.cancel();
      });
      return;
    }
    const o = ha.has(l);
    o && this.onBindTransform && this.onBindTransform();
    const c = u.on("change", (h) => {
      this.latestValues[l] = h, this.props.onUpdate && Ot.preRender(this.notifyUpdate), o && this.projection && (this.projection.isTransformDirty = !0), this.scheduleRender();
    });
    let d;
    typeof window < "u" && window.MotionCheckAppearSync && (d = window.MotionCheckAppearSync(this, l, u)), this.valueSubscriptions.set(l, () => {
      c(), d && d();
    });
  }
  sortNodePosition(l) {
    return !this.current || !this.sortInstanceNodePosition || this.type !== l.type ? 0 : this.sortInstanceNodePosition(this.current, l.current);
  }
  updateFeatures() {
    let l = "animation";
    for (l in ru) {
      const u = ru[l];
      if (!u)
        continue;
      const { isEnabled: o, Feature: c } = u;
      if (!this.features[l] && c && o(this.props) && (this.features[l] = new c(this)), this.features[l]) {
        const d = this.features[l];
        d.isMounted ? d.update() : (d.mount(), d.isMounted = !0);
      }
    }
  }
  triggerBuild() {
    this.build(this.renderState, this.latestValues, this.props);
  }
  /**
   * Measure the current viewport box with or without transforms.
   * Only measures axis-aligned boxes, rotate and skew must be manually
   * removed with a re-render to work.
   */
  measureViewportBox() {
    return this.current ? this.measureInstanceViewportBox(this.current, this.props) : kt();
  }
  getStaticValue(l) {
    return this.latestValues[l];
  }
  setStaticValue(l, u) {
    this.latestValues[l] = u;
  }
  /**
   * Update the provided props. Ensure any newly-added motion values are
   * added to our map, old ones removed, and listeners updated.
   */
  update(l, u) {
    (l.transformTemplate || this.props.transformTemplate) && this.scheduleRender(), this.prevProps = this.props, this.props = l, this.prevPresenceContext = this.presenceContext, this.presenceContext = u;
    for (let o = 0; o < Gy.length; o++) {
      const c = Gy[o];
      this.propEventSubscriptions[c] && (this.propEventSubscriptions[c](), delete this.propEventSubscriptions[c]);
      const d = "on" + c, h = l[d];
      h && (this.propEventSubscriptions[c] = this.on(c, h));
    }
    this.prevMotionValues = _b(this, this.scrapeMotionValuesFromProps(l, this.prevProps || {}, this), this.prevMotionValues), this.handleChildMotionValue && this.handleChildMotionValue();
  }
  getProps() {
    return this.props;
  }
  /**
   * Returns the variant definition with a given name.
   */
  getVariant(l) {
    return this.props.variants ? this.props.variants[l] : void 0;
  }
  /**
   * Returns the defined default transition on this component.
   */
  getDefaultTransition() {
    return this.props.transition;
  }
  getTransformPagePoint() {
    return this.props.transformPagePoint;
  }
  getClosestVariantNode() {
    return this.isVariantNode ? this : this.parent ? this.parent.getClosestVariantNode() : void 0;
  }
  /**
   * Add a child visual element to our set of children.
   */
  addVariantChild(l) {
    const u = this.getClosestVariantNode();
    if (u)
      return u.variantChildren && u.variantChildren.add(l), () => u.variantChildren.delete(l);
  }
  /**
   * Add a motion value and bind it to this visual element.
   */
  addValue(l, u) {
    const o = this.values.get(l);
    u !== o && (o && this.removeValue(l), this.bindToMotionValue(l, u), this.values.set(l, u), this.latestValues[l] = u.get());
  }
  /**
   * Remove a motion value and unbind any active subscriptions.
   */
  removeValue(l) {
    this.values.delete(l);
    const u = this.valueSubscriptions.get(l);
    u && (u(), this.valueSubscriptions.delete(l)), delete this.latestValues[l], this.removeValueFromRenderState(l, this.renderState);
  }
  /**
   * Check whether we have a motion value for this key
   */
  hasValue(l) {
    return this.values.has(l);
  }
  getValue(l, u) {
    if (this.props.values && this.props.values[l])
      return this.props.values[l];
    let o = this.values.get(l);
    return o === void 0 && u !== void 0 && (o = ra(u === null ? void 0 : u, { owner: this }), this.addValue(l, o)), o;
  }
  /**
   * If we're trying to animate to a previously unencountered value,
   * we need to check for it in our state and as a last resort read it
   * directly from the instance (which might have performance implications).
   */
  readValue(l, u) {
    let o = this.latestValues[l] !== void 0 || !this.current ? this.latestValues[l] : this.getBaseTargetFromProps(this.props, l) ?? this.readValueFromInstance(this.current, l, this.options);
    return o != null && (typeof o == "string" && (wp(o) || Hp(o)) ? o = parseFloat(o) : !Ob(o) && Qe.test(u) && (o = Rg(l, u)), this.setBaseTarget(l, ae(o) ? o.get() : o)), ae(o) ? o.get() : o;
  }
  /**
   * Set the base target to later animate back to. This is currently
   * only hydrated on creation and when we first read a value.
   */
  setBaseTarget(l, u) {
    this.baseTarget[l] = u;
  }
  /**
   * Find the base target for a value thats been removed from all animation
   * props.
   */
  getBaseTarget(l) {
    const { initial: u } = this.props;
    let o;
    if (typeof u == "string" || typeof u == "object") {
      const d = Fc(this.props, u, this.presenceContext?.custom);
      d && (o = d[l]);
    }
    if (u && o !== void 0)
      return o;
    const c = this.getBaseTargetFromProps(this.props, l);
    return c !== void 0 && !ae(c) ? c : this.initialValues[l] !== void 0 && o === void 0 ? void 0 : this.baseTarget[l];
  }
  on(l, u) {
    return this.events[l] || (this.events[l] = new jc()), this.events[l].add(u);
  }
  notify(l, ...u) {
    this.events[l] && this.events[l].notify(...u);
  }
  scheduleRenderMicrotask() {
    $c.render(this.render);
  }
}
class Lg extends jb {
  constructor() {
    super(...arguments), this.KeyframeResolver = cb;
  }
  sortInstanceNodePosition(l, u) {
    return l.compareDocumentPosition(u) & 2 ? 1 : -1;
  }
  getBaseTargetFromProps(l, u) {
    const o = l.style;
    return o ? o[u] : void 0;
  }
  removeValueFromRenderState(l, { vars: u, style: o }) {
    delete u[l], delete o[l];
  }
  handleChildMotionValue() {
    this.childSubscription && (this.childSubscription(), delete this.childSubscription);
    const { children: l } = this.props;
    ae(l) && (this.childSubscription = l.on("change", (u) => {
      this.current && (this.current.textContent = `${u}`);
    }));
  }
}
class kn {
  constructor(l) {
    this.isMounted = !1, this.node = l;
  }
  update() {
  }
}
function Hg({ top: i, left: l, right: u, bottom: o }) {
  return {
    x: { min: l, max: u },
    y: { min: i, max: o }
  };
}
function wb({ x: i, y: l }) {
  return { top: l.min, right: i.max, bottom: l.max, left: i.min };
}
function Lb(i, l) {
  if (!l)
    return i;
  const u = l({ x: i.left, y: i.top }), o = l({ x: i.right, y: i.bottom });
  return {
    top: u.y,
    left: u.x,
    bottom: o.y,
    right: o.x
  };
}
function $r(i) {
  return i === void 0 || i === 1;
}
function Dc({ scale: i, scaleX: l, scaleY: u }) {
  return !$r(i) || !$r(l) || !$r(u);
}
function yi(i) {
  return Dc(i) || Yg(i) || i.z || i.rotate || i.rotateX || i.rotateY || i.skewX || i.skewY;
}
function Yg(i) {
  return Xy(i.x) || Xy(i.y);
}
function Xy(i) {
  return i && i !== "0%";
}
function cu(i, l, u) {
  const o = i - u, c = l * o;
  return u + c;
}
function Zy(i, l, u, o, c) {
  return c !== void 0 && (i = cu(i, c, o)), cu(i, u, o) + l;
}
function Cc(i, l = 0, u = 1, o, c) {
  i.min = Zy(i.min, l, u, o, c), i.max = Zy(i.max, l, u, o, c);
}
function qg(i, { x: l, y: u }) {
  Cc(i.x, l.translate, l.scale, l.originPoint), Cc(i.y, u.translate, u.scale, u.originPoint);
}
const Qy = 0.999999999999, Ky = 1.0000000000001;
function Hb(i, l, u, o = !1) {
  const c = u.length;
  if (!c)
    return;
  l.x = l.y = 1;
  let d, h;
  for (let y = 0; y < c; y++) {
    d = u[y], h = d.projectionDelta;
    const { visualElement: g } = d.options;
    g && g.props.style && g.props.style.display === "contents" || (o && d.options.layoutScroll && d.scroll && d !== d.root && (Pe(i.x, -d.scroll.offset.x), Pe(i.y, -d.scroll.offset.y)), h && (l.x *= h.x.scale, l.y *= h.y.scale, qg(i, h)), o && yi(d.latestValues) && tu(i, d.latestValues, d.layout?.layoutBox));
  }
  l.x < Ky && l.x > Qy && (l.x = 1), l.y < Ky && l.y > Qy && (l.y = 1);
}
function Pe(i, l) {
  i.min += l, i.max += l;
}
function Jy(i, l, u, o, c = 0.5) {
  const d = Rt(i.min, i.max, c);
  Cc(i, l, u, d, o);
}
function ky(i, l) {
  return typeof i == "string" ? parseFloat(i) / 100 * (l.max - l.min) : i;
}
function tu(i, l, u) {
  const o = u ?? i;
  Jy(i.x, ky(l.x, o.x), l.scaleX, l.scale, l.originX), Jy(i.y, ky(l.y, o.y), l.scaleY, l.scale, l.originY);
}
function Gg(i, l) {
  return Hg(Lb(i.getBoundingClientRect(), l));
}
function Yb(i, l, u) {
  const o = Gg(i, u), { scroll: c } = l;
  return c && (Pe(o.x, c.offset.x), Pe(o.y, c.offset.y)), o;
}
const qb = {
  x: "translateX",
  y: "translateY",
  z: "translateZ",
  transformPerspective: "perspective"
}, Gb = fa.length;
function Xb(i, l, u) {
  let o = "", c = !0;
  for (let h = 0; h < Gb; h++) {
    const y = fa[h], g = i[y];
    if (g === void 0)
      continue;
    let m = !0;
    if (typeof g == "number")
      m = g === (y.startsWith("scale") ? 1 : 0);
    else {
      const v = parseFloat(g);
      m = y.startsWith("scale") ? v === 1 : v === 0;
    }
    if (!m || u) {
      const v = xc(g, ou[y]);
      if (!m) {
        c = !1;
        const S = qb[y] || y;
        o += `${S}(${v}) `;
      }
      u && (l[y] = v);
    }
  }
  const d = i.pathRotation;
  return d && (c = !1, o += `rotate(${xc(d, ou.pathRotation)}) `), o = o.trim(), u ? o = u(l, c ? "" : o) : c && (o = "none"), o;
}
function af(i, l, u) {
  const { style: o, vars: c, transformOrigin: d } = i;
  let h = !1, y = !1;
  for (const g in l) {
    const m = l[g];
    if (ha.has(g)) {
      h = !0;
      continue;
    } else if (tg(g)) {
      c[g] = m;
      continue;
    } else {
      const v = xc(m, ou[g]);
      g.startsWith("origin") ? (y = !0, d[g] = v) : o[g] = v;
    }
  }
  if (l.transform || (h || u ? o.transform = Xb(l, i.transform, u) : o.transform && (o.transform = "none")), y) {
    const { originX: g = "50%", originY: m = "50%", originZ: v = 0 } = d;
    o.transformOrigin = `${g} ${m} ${v}`;
  }
}
function Xg(i, { style: l, vars: u }, o, c) {
  const d = i.style;
  let h;
  for (h in l)
    d[h] = l[h];
  c?.applyProjectionStyles(d, o);
  for (h in u)
    d.setProperty(h, u[h]);
}
function Fy(i, l) {
  return l.max === l.min ? 0 : i / (l.max - l.min) * 100;
}
const ol = {
  correct: (i, l) => {
    if (!l.target)
      return i;
    if (typeof i == "string")
      if (F.test(i))
        i = parseFloat(i);
      else
        return i;
    const u = Fy(i, l.target.x), o = Fy(i, l.target.y);
    return `${u}% ${o}%`;
  }
}, Zb = {
  correct: (i, { treeScale: l, projectionDelta: u }) => {
    const o = i, c = Qe.parse(i);
    if (c.length > 5)
      return o;
    const d = Qe.createTransformer(i), h = typeof c[0] != "number" ? 1 : 0, y = u.x.scale * l.x, g = u.y.scale * l.y;
    c[0 + h] /= y, c[1 + h] /= g;
    const m = Rt(y, g, 0.5);
    return typeof c[2 + h] == "number" && (c[2 + h] /= m), typeof c[3 + h] == "number" && (c[3 + h] /= m), d(c);
  }
}, zc = {
  borderRadius: {
    ...ol,
    applyTo: [...Pc]
  },
  borderTopLeftRadius: ol,
  borderTopRightRadius: ol,
  borderBottomLeftRadius: ol,
  borderBottomRightRadius: ol,
  boxShadow: Zb
};
function Zg(i, { layout: l, layoutId: u }) {
  return ha.has(i) || i.startsWith("origin") || (l || u !== void 0) && (!!zc[i] || i === "opacity");
}
function lf(i, l, u) {
  const o = i.style, c = l?.style, d = {};
  if (!o)
    return d;
  for (const h in o)
    (ae(o[h]) || c && ae(c[h]) || Zg(h, i) || u?.getValue(h)?.liveStyle !== void 0) && (d[h] = o[h]);
  return d;
}
function Qb(i) {
  return window.getComputedStyle(i);
}
class Kb extends Lg {
  constructor() {
    super(...arguments), this.type = "html", this.renderInstance = Xg;
  }
  mount(l) {
    yu(!!l.style), super.mount(l);
  }
  readValueFromInstance(l, u) {
    if (ha.has(u))
      return this.projection?.isProjecting ? dc(u) : hT(l, u);
    {
      const o = Qb(l), c = (tg(u) ? o.getPropertyValue(u) : o[u]) || 0;
      return typeof c == "string" ? c.trim() : c;
    }
  }
  measureInstanceViewportBox(l, { transformPagePoint: u }) {
    return Gg(l, u);
  }
  build(l, u, o) {
    af(l, u, o.transformTemplate);
  }
  scrapeMotionValuesFromProps(l, u, o) {
    return lf(l, u, o);
  }
}
const Jb = {
  offset: "stroke-dashoffset",
  array: "stroke-dasharray"
}, kb = {
  offset: "strokeDashoffset",
  array: "strokeDasharray"
};
function Fb(i, l, u = 1, o = 0, c = !0) {
  i.pathLength = 1;
  const d = c ? Jb : kb;
  i[d.offset] = `${-o}`, i[d.array] = `${l} ${u}`;
}
const Wb = [
  "offsetDistance",
  "offsetPath",
  "offsetRotate",
  "offsetAnchor"
];
function Qg(i, {
  attrX: l,
  attrY: u,
  attrScale: o,
  pathLength: c,
  pathSpacing: d = 1,
  pathOffset: h = 0,
  // This is object creation, which we try to avoid per-frame.
  ...y
}, g, m, v) {
  if (af(i, y, m), g) {
    i.style.viewBox && (i.attrs.viewBox = i.style.viewBox);
    return;
  }
  i.attrs = i.style, i.style = {};
  const { attrs: S, style: b } = i;
  S.transform && (b.transform = S.transform, delete S.transform), (b.transform || S.transformOrigin) && (b.transformOrigin = S.transformOrigin ?? "50% 50%", delete S.transformOrigin), b.transform && (b.transformBox = v?.transformBox ?? "fill-box", delete S.transformBox);
  for (const _ of Wb)
    S[_] !== void 0 && (b[_] = S[_], delete S[_]);
  l !== void 0 && (S.x = l), u !== void 0 && (S.y = u), o !== void 0 && (S.scale = o), c !== void 0 && Fb(S, c, d, h, !1);
}
const Kg = /* @__PURE__ */ new Set([
  "baseFrequency",
  "diffuseConstant",
  "kernelMatrix",
  "kernelUnitLength",
  "keySplines",
  "keyTimes",
  "limitingConeAngle",
  "markerHeight",
  "markerWidth",
  "numOctaves",
  "targetX",
  "targetY",
  "surfaceScale",
  "specularConstant",
  "specularExponent",
  "stdDeviation",
  "tableValues",
  "viewBox",
  "gradientTransform",
  "pathLength",
  "startOffset",
  "textLength",
  "lengthAdjust"
]), Jg = (i) => typeof i == "string" && i.toLowerCase() === "svg";
function Pb(i, l, u, o) {
  Xg(i, l, void 0, o);
  for (const c in l.attrs)
    i.setAttribute(Kg.has(c) ? c : Wc(c), l.attrs[c]);
}
function kg(i, l, u) {
  const o = lf(i, l, u);
  for (const c in i)
    if (ae(i[c]) || ae(l[c])) {
      const d = fa.indexOf(c) !== -1 ? "attr" + c.charAt(0).toUpperCase() + c.substring(1) : c;
      o[d] = i[c];
    }
  return o;
}
class $b extends Lg {
  constructor() {
    super(...arguments), this.type = "svg", this.isSVGTag = !1, this.measureInstanceViewportBox = kt;
  }
  getBaseTargetFromProps(l, u) {
    return l[u];
  }
  readValueFromInstance(l, u) {
    if (ha.has(u)) {
      const o = zg(u);
      return o && o.default || 0;
    }
    return u = Kg.has(u) ? u : Wc(u), l.getAttribute(u);
  }
  scrapeMotionValuesFromProps(l, u, o) {
    return kg(l, u, o);
  }
  build(l, u, o) {
    Qg(l, u, this.isSVGTag, o.transformTemplate, o.style);
  }
  renderInstance(l, u, o, c) {
    Pb(l, u, o, c);
  }
  mount(l) {
    this.isSVGTag = Jg(l.tagName), super.mount(l);
  }
}
const Ib = nf.length;
function Fg(i) {
  if (!i)
    return;
  if (!i.isControllingVariants) {
    const u = i.parent ? Fg(i.parent) || {} : {};
    return i.props.initial !== void 0 && (u.initial = i.props.initial), u;
  }
  const l = {};
  for (let u = 0; u < Ib; u++) {
    const o = nf[u], c = i.props[o];
    (pl(c) || c === !1) && (l[o] = c);
  }
  return l;
}
function Wg(i, l) {
  if (!Array.isArray(l))
    return !1;
  const u = l.length;
  if (u !== i.length)
    return !1;
  for (let o = 0; o < u; o++)
    if (l[o] !== i[o])
      return !1;
  return !0;
}
const t2 = [...ef].reverse(), e2 = ef.length;
function n2(i) {
  return (l) => Promise.all(l.map(({ animation: u, options: o }) => IT(i, u, o)));
}
function i2(i) {
  let l = n2(i), u = Wy(), o = !0, c = !1;
  const d = (m) => (v, S) => {
    const b = Si(i, S, m === "exit" ? i.presenceContext?.custom : void 0);
    if (b) {
      const { transition: _, transitionEnd: z, ...j } = b;
      v = { ...v, ...j, ...z };
    }
    return v;
  };
  function h(m) {
    l = m(i);
  }
  function y(m) {
    const { props: v } = i, S = Fg(i.parent) || {}, b = [], _ = /* @__PURE__ */ new Set();
    let z = {}, j = 1 / 0;
    for (let L = 0; L < e2; L++) {
      const G = t2[L], H = u[G], Y = v[G] !== void 0 ? v[G] : S[G], tt = pl(Y), nt = G === m ? H.isActive : null;
      nt === !1 && (j = L);
      let Q = Y === S[G] && Y !== v[G] && tt;
      if (Q && (o || c) && i.manuallyAnimateOnMount && (Q = !1), H.protectedKeys = { ...z }, // If it isn't active and hasn't *just* been set as inactive
      !H.isActive && nt === null || // If we didn't and don't have any defined prop for this animation type
      !Y && !H.prevProp || // Or if the prop doesn't define an animation
      gu(Y) || typeof Y == "boolean")
        continue;
      if (G === "exit" && H.isActive && nt !== !0) {
        H.prevResolvedValues && (z = {
          ...z,
          ...H.prevResolvedValues
        });
        continue;
      }
      const K = a2(H.prevProp, Y);
      let it = K || // If we're making this variant active, we want to always make it active
      G === m && H.isActive && !Q && tt || // If we removed a higher-priority variant (i is in reverse order)
      L > j && tt, $ = !1;
      const yt = Array.isArray(Y) ? Y : [Y];
      let vt = yt.reduce(d(G), {});
      nt === !1 && (vt = {});
      const { prevResolvedValues: Pt = {} } = H, qt = {
        ...Pt,
        ...vt
      }, wt = (J) => {
        it = !0, _.has(J) && ($ = !0, _.delete(J)), H.needsAnimating[J] = !0;
        const ut = i.getValue(J);
        ut && (ut.liveStyle = !1);
      };
      for (const J in qt) {
        const ut = vt[J], pt = Pt[J];
        if (z.hasOwnProperty(J))
          continue;
        let E = !1;
        Sc(ut) && Sc(pt) ? E = !Wg(ut, pt) || K : E = ut !== pt, E ? ut != null ? wt(J) : _.add(J) : ut !== void 0 && _.has(J) ? wt(J) : H.protectedKeys[J] = !0;
      }
      H.prevProp = Y, H.prevResolvedValues = vt, H.isActive && (z = { ...z, ...vt }), (o || c) && i.blockInitialAnimation && (it = !1);
      const O = Q && K;
      it && (!O || $) && b.push(...yt.map((J) => {
        const ut = { type: G };
        if (typeof J == "string" && (o || c) && !O && i.manuallyAnimateOnMount && i.parent) {
          const { parent: pt } = i, E = Si(pt, J);
          if (pt.enteringChildren && E) {
            const { delayChildren: N } = E.transition || {};
            ut.delay = Tg(pt.enteringChildren, i, N);
          }
        }
        return {
          animation: J,
          options: ut
        };
      }));
    }
    if (_.size) {
      const L = {};
      if (typeof v.initial != "boolean") {
        const G = Si(i, Array.isArray(v.initial) ? v.initial[0] : v.initial);
        G && G.transition && (L.transition = G.transition);
      }
      _.forEach((G) => {
        const H = i.getBaseTarget(G), Y = i.getValue(G);
        Y && (Y.liveStyle = !0), L[G] = H ?? null;
      }), b.push({ animation: L });
    }
    let w = !!b.length;
    return o && (v.initial === !1 || v.initial === v.animate) && !i.manuallyAnimateOnMount && (w = !1), o = !1, c = !1, w ? l(b) : Promise.resolve();
  }
  function g(m, v) {
    if (u[m].isActive === v)
      return Promise.resolve();
    i.variantChildren?.forEach((b) => b.animationState?.setActive(m, v)), u[m].isActive = v;
    const S = y(m);
    for (const b in u)
      u[b].protectedKeys = {};
    return S;
  }
  return {
    animateChanges: y,
    setActive: g,
    setAnimateFunction: h,
    getState: () => u,
    reset: () => {
      u = Wy(), c = !0;
    }
  };
}
function a2(i, l) {
  return typeof l == "string" ? l !== i : Array.isArray(l) ? !Wg(l, i) : !1;
}
function mi(i = !1) {
  return {
    isActive: i,
    protectedKeys: {},
    needsAnimating: {},
    prevResolvedValues: {}
  };
}
function Wy() {
  return {
    animate: mi(!0),
    whileInView: mi(),
    whileHover: mi(),
    whileTap: mi(),
    whileDrag: mi(),
    whileFocus: mi(),
    exit: mi()
  };
}
function Rc(i, l) {
  i.min = l.min, i.max = l.max;
}
function Xe(i, l) {
  Rc(i.x, l.x), Rc(i.y, l.y);
}
function Py(i, l) {
  i.translate = l.translate, i.scale = l.scale, i.originPoint = l.originPoint, i.origin = l.origin;
}
const Pg = 1e-4, l2 = 1 - Pg, s2 = 1 + Pg, $g = 0.01, u2 = 0 - $g, o2 = 0 + $g;
function re(i) {
  return i.max - i.min;
}
function r2(i, l, u) {
  return Math.abs(i - l) <= u;
}
function $y(i, l, u, o = 0.5) {
  i.origin = o, i.originPoint = Rt(l.min, l.max, i.origin), i.scale = re(u) / re(l), i.translate = Rt(u.min, u.max, i.origin) - i.originPoint, (i.scale >= l2 && i.scale <= s2 || isNaN(i.scale)) && (i.scale = 1), (i.translate >= u2 && i.translate <= o2 || isNaN(i.translate)) && (i.translate = 0);
}
function hl(i, l, u, o) {
  $y(i.x, l.x, u.x, o ? o.originX : void 0), $y(i.y, l.y, u.y, o ? o.originY : void 0);
}
function Iy(i, l, u, o = 0) {
  const c = o ? Rt(u.min, u.max, o) : u.min;
  i.min = c + l.min, i.max = i.min + re(l);
}
function c2(i, l, u, o) {
  Iy(i.x, l.x, u.x, o?.x), Iy(i.y, l.y, u.y, o?.y);
}
function tp(i, l, u, o = 0) {
  const c = o ? Rt(u.min, u.max, o) : u.min;
  i.min = l.min - c, i.max = i.min + re(l);
}
function fu(i, l, u, o) {
  tp(i.x, l.x, u.x, o?.x), tp(i.y, l.y, u.y, o?.y);
}
function ep(i, l, u, o, c) {
  return i -= l, i = cu(i, 1 / u, o), c !== void 0 && (i = cu(i, 1 / c, o)), i;
}
function f2(i, l = 0, u = 1, o = 0.5, c, d = i, h = i) {
  if ($e.test(l) && (l = parseFloat(l), l = Rt(h.min, h.max, l / 100) - h.min), typeof l != "number")
    return;
  let y = Rt(d.min, d.max, o);
  i === d && (y -= l), i.min = ep(i.min, l, u, y, c), i.max = ep(i.max, l, u, y, c);
}
function np(i, l, [u, o, c], d, h) {
  f2(i, l[u], l[o], l[c], l.scale, d, h);
}
const h2 = ["x", "scaleX", "originX"], d2 = ["y", "scaleY", "originY"];
function ip(i, l, u, o) {
  np(i.x, l, h2, u ? u.x : void 0, o ? o.x : void 0), np(i.y, l, d2, u ? u.y : void 0, o ? o.y : void 0);
}
function ap(i) {
  return i.translate === 0 && i.scale === 1;
}
function Ig(i) {
  return ap(i.x) && ap(i.y);
}
function lp(i, l) {
  return i.min === l.min && i.max === l.max;
}
function m2(i, l) {
  return lp(i.x, l.x) && lp(i.y, l.y);
}
function sp(i, l) {
  return Math.round(i.min) === Math.round(l.min) && Math.round(i.max) === Math.round(l.max);
}
function t0(i, l) {
  return sp(i.x, l.x) && sp(i.y, l.y);
}
function up(i) {
  return re(i.x) / re(i.y);
}
function op(i, l) {
  return i.translate === l.translate && i.scale === l.scale && i.originPoint === l.originPoint;
}
function We(i) {
  return [i("x"), i("y")];
}
function y2(i, l, u) {
  let o = "";
  const c = i.x.translate / l.x, d = i.y.translate / l.y, h = u?.z || 0;
  if ((c || d || h) && (o = `translate3d(${c}px, ${d}px, ${h}px) `), (l.x !== 1 || l.y !== 1) && (o += `scale(${1 / l.x}, ${1 / l.y}) `), u) {
    const { transformPerspective: m, rotate: v, pathRotation: S, rotateX: b, rotateY: _, skewX: z, skewY: j } = u;
    m && (o = `perspective(${m}px) ${o}`), v && (o += `rotate(${v}deg) `), S && (o += `rotate(${S}deg) `), b && (o += `rotateX(${b}deg) `), _ && (o += `rotateY(${_}deg) `), z && (o += `skewX(${z}deg) `), j && (o += `skewY(${j}deg) `);
  }
  const y = i.x.scale * l.x, g = i.y.scale * l.y;
  return (y !== 1 || g !== 1) && (o += `scale(${y}, ${g})`), o || "none";
}
const p2 = Pc.length, rp = (i) => typeof i == "string" ? parseFloat(i) : i, cp = (i) => typeof i == "number" || F.test(i);
function g2(i, l, u, o, c, d) {
  c ? (i.opacity = Rt(0, u.opacity ?? 1, v2(o)), i.opacityExit = Rt(l.opacity ?? 1, 0, S2(o))) : d && (i.opacity = Rt(l.opacity ?? 1, u.opacity ?? 1, o));
  for (let h = 0; h < p2; h++) {
    const y = Pc[h];
    let g = fp(l, y), m = fp(u, y);
    if (g === void 0 && m === void 0)
      continue;
    g || (g = 0), m || (m = 0), g === 0 || m === 0 || cp(g) === cp(m) ? (i[y] = Math.max(Rt(rp(g), rp(m), o), 0), ($e.test(m) || $e.test(g)) && (i[y] += "%")) : i[y] = m;
  }
  (l.rotate || u.rotate) && (i.rotate = Rt(l.rotate || 0, u.rotate || 0, o));
}
function fp(i, l) {
  return i[l] !== void 0 ? i[l] : i.borderRadius;
}
const v2 = /* @__PURE__ */ e0(0, 0.5, kp), S2 = /* @__PURE__ */ e0(0.5, 0.95, He);
function e0(i, l, u) {
  return (o) => o < i ? 0 : o > l ? 1 : u(/* @__PURE__ */ ml(i, l, o));
}
function T2(i, l, u) {
  const o = ae(i) ? i : ra(i);
  return o.start(kc("", o, l, u)), o.animation;
}
function gl(i, l, u, o = { passive: !0 }) {
  return i.addEventListener(l, u, o), () => i.removeEventListener(l, u, o);
}
const b2 = (i, l) => i.depth - l.depth;
class A2 {
  constructor() {
    this.children = [], this.isDirty = !1;
  }
  add(l) {
    Nc(this.children, l), this.isDirty = !0;
  }
  remove(l) {
    iu(this.children, l), this.isDirty = !0;
  }
  forEach(l) {
    this.isDirty && this.children.sort(b2), this.isDirty = !1, this.children.forEach(l);
  }
}
function E2(i, l) {
  const u = oe.now(), o = ({ timestamp: c }) => {
    const d = c - u;
    d >= l && (Jn(o), i(d - l));
  };
  return Ot.setup(o, !0), () => Jn(o);
}
function eu(i) {
  return ae(i) ? i.get() : i;
}
class x2 {
  constructor() {
    this.members = [];
  }
  add(l) {
    Nc(this.members, l);
    for (let u = this.members.length - 1; u >= 0; u--) {
      const o = this.members[u];
      if (o === l || o === this.lead || o === this.prevLead)
        continue;
      const c = o.instance;
      (!c || c.isConnected === !1) && !o.snapshot && (iu(this.members, o), o.unmount());
    }
    l.scheduleRender();
  }
  remove(l) {
    if (iu(this.members, l), l === this.prevLead && (this.prevLead = void 0), l === this.lead) {
      const u = this.members[this.members.length - 1];
      u && this.promote(u);
    }
  }
  relegate(l) {
    for (let u = this.members.indexOf(l) - 1; u >= 0; u--) {
      const o = this.members[u];
      if (o.isPresent !== !1 && o.instance?.isConnected !== !1)
        return this.promote(o), !0;
    }
    return !1;
  }
  promote(l, u) {
    const o = this.lead;
    if (l !== o && (this.prevLead = o, this.lead = l, l.show(), o)) {
      o.updateSnapshot(), l.scheduleRender();
      const { layoutDependency: c } = o.options, { layoutDependency: d } = l.options;
      (c === void 0 || c !== d) && (l.resumeFrom = o, u && (o.preserveOpacity = !0), o.snapshot && (l.snapshot = o.snapshot, l.snapshot.latestValues = o.animationValues || o.latestValues), l.root?.isUpdating && (l.isLayoutDirty = !0)), l.options.crossfade === !1 && o.hide();
    }
  }
  exitAnimationComplete() {
    this.members.forEach((l) => {
      l.options.onExitComplete?.(), l.resumingFrom?.options.onExitComplete?.();
    });
  }
  scheduleRender() {
    this.members.forEach((l) => l.instance && l.scheduleRender(!1));
  }
  removeLeadSnapshot() {
    this.lead?.snapshot && (this.lead.snapshot = void 0);
  }
}
const nu = {
  /**
   * Global flag as to whether the tree has animated since the last time
   * we resized the window
   */
  hasAnimatedSinceResize: !0,
  /**
   * We set this to true once, on the first update. Any nodes added to the tree beyond that
   * update will be given a `data-projection-id` attribute.
   */
  hasEverUpdated: !1
}, Ir = ["", "X", "Y", "Z"], M2 = 1e3;
let D2 = 0;
function tc(i, l, u, o) {
  const { latestValues: c } = l;
  c[i] && (u[i] = c[i], l.setStaticValue(i, 0), o && (o[i] = 0));
}
function n0(i) {
  if (i.hasCheckedOptimisedAppear = !0, i.root === i)
    return;
  const { visualElement: l } = i.options;
  if (!l)
    return;
  const u = xg(l);
  if (window.MotionHasOptimisedAnimation(u, "transform")) {
    const { layout: c, layoutId: d } = i.options;
    window.MotionCancelOptimisedAnimation(u, "transform", Ot, !(c || d));
  }
  const { parent: o } = i;
  o && !o.hasCheckedOptimisedAppear && n0(o);
}
function i0({ attachResizeListener: i, defaultParent: l, measureScroll: u, checkIsScrollRoot: o, resetTransform: c }) {
  return class {
    constructor(h = {}, y = l?.()) {
      this.id = D2++, this.animationId = 0, this.animationCommitId = 0, this.children = /* @__PURE__ */ new Set(), this.options = {}, this.isTreeAnimating = !1, this.isAnimationBlocked = !1, this.isLayoutDirty = !1, this.isProjectionDirty = !1, this.isSharedProjectionDirty = !1, this.isTransformDirty = !1, this.updateManuallyBlocked = !1, this.updateBlockedByResize = !1, this.isUpdating = !1, this.isSVG = !1, this.needsReset = !1, this.shouldResetTransform = !1, this.hasCheckedOptimisedAppear = !1, this.treeScale = { x: 1, y: 1 }, this.eventHandlers = /* @__PURE__ */ new Map(), this.hasTreeAnimated = !1, this.layoutVersion = 0, this.updateScheduled = !1, this.scheduleUpdate = () => this.update(), this.projectionUpdateScheduled = !1, this.checkUpdateFailed = () => {
        this.isUpdating && (this.isUpdating = !1, this.clearAllSnapshots());
      }, this.updateProjection = () => {
        this.projectionUpdateScheduled = !1, this.nodes.forEach(R2), this.nodes.forEach(N2), this.nodes.forEach(j2), this.nodes.forEach(O2);
      }, this.resolvedRelativeTargetAt = 0, this.linkedParentVersion = 0, this.hasProjected = !1, this.isVisible = !0, this.animationProgress = 0, this.sharedNodes = /* @__PURE__ */ new Map(), this.latestValues = h, this.root = y ? y.root || y : this, this.path = y ? [...y.path, y] : [], this.parent = y, this.depth = y ? y.depth + 1 : 0;
      for (let g = 0; g < this.path.length; g++)
        this.path[g].shouldResetTransform = !0;
      this.root === this && (this.nodes = new A2());
    }
    addEventListener(h, y) {
      return this.eventHandlers.has(h) || this.eventHandlers.set(h, new jc()), this.eventHandlers.get(h).add(y);
    }
    notifyListeners(h, ...y) {
      const g = this.eventHandlers.get(h);
      g && g.notify(...y);
    }
    hasListeners(h) {
      return this.eventHandlers.has(h);
    }
    /**
     * Lifecycles
     */
    mount(h) {
      if (this.instance)
        return;
      this.isSVG = tf(h) && !zb(h), this.instance = h;
      const { layoutId: y, layout: g, visualElement: m } = this.options;
      if (m && !m.current && m.mount(h), this.root.nodes.add(this), this.parent && this.parent.children.add(this), this.root.hasTreeAnimated && (g || y) && (this.isLayoutDirty = !0), i) {
        let v, S = 0;
        const b = () => this.root.updateBlockedByResize = !1;
        Ot.read(() => {
          S = window.innerWidth;
        }), i(h, () => {
          const _ = window.innerWidth;
          _ !== S && (S = _, this.root.updateBlockedByResize = !0, v && v(), v = E2(b, 250), nu.hasAnimatedSinceResize && (nu.hasAnimatedSinceResize = !1, this.nodes.forEach(mp)));
        });
      }
      y && this.root.registerSharedNode(y, this), this.options.animate !== !1 && m && (y || g) && this.addEventListener("didUpdate", ({ delta: v, hasLayoutChanged: S, hasRelativeLayoutChanged: b, layout: _ }) => {
        if (this.isTreeAnimationBlocked()) {
          this.target = void 0, this.relativeTarget = void 0;
          return;
        }
        const z = this.options.transition || m.getDefaultTransition() || q2, { onLayoutAnimationStart: j, onLayoutAnimationComplete: w } = m.getProps(), L = !this.targetLayout || !t0(this.targetLayout, _), G = !S && b;
        if (this.options.layoutRoot || this.resumeFrom || G || S && (L || !this.currentAnimation)) {
          this.resumeFrom && (this.resumingFrom = this.resumeFrom, this.resumingFrom.resumingFrom = void 0);
          const H = {
            ...Jc(z, "layout"),
            onPlay: j,
            onComplete: w
          };
          (m.shouldReduceMotion || this.options.layoutRoot) && (H.delay = 0, H.type = !1), this.startAnimation(H), this.setAnimationOrigin(v, G, H.path);
        } else
          S || mp(this), this.isLead() && this.options.onExitComplete && this.options.onExitComplete();
        this.targetLayout = _;
      });
    }
    unmount() {
      this.options.layoutId && this.willUpdate(), this.root.nodes.remove(this);
      const h = this.getStack();
      h && h.remove(this), this.parent && this.parent.children.delete(this), this.instance = void 0, this.eventHandlers.clear(), Jn(this.updateProjection);
    }
    // only on the root
    blockUpdate() {
      this.updateManuallyBlocked = !0;
    }
    unblockUpdate() {
      this.updateManuallyBlocked = !1;
    }
    isUpdateBlocked() {
      return this.updateManuallyBlocked || this.updateBlockedByResize;
    }
    isTreeAnimationBlocked() {
      return this.isAnimationBlocked || this.parent && this.parent.isTreeAnimationBlocked() || !1;
    }
    // Note: currently only running on root node
    startUpdate() {
      this.isUpdateBlocked() || (this.isUpdating = !0, this.nodes && this.nodes.forEach(w2), this.animationId++);
    }
    getTransformTemplate() {
      const { visualElement: h } = this.options;
      return h && h.getProps().transformTemplate;
    }
    willUpdate(h = !0) {
      if (this.root.hasTreeAnimated = !0, this.root.isUpdateBlocked()) {
        this.options.onExitComplete && this.options.onExitComplete();
        return;
      }
      if (window.MotionCancelOptimisedAnimation && !this.hasCheckedOptimisedAppear && n0(this), !this.root.isUpdating && this.root.startUpdate(), this.isLayoutDirty)
        return;
      this.isLayoutDirty = !0;
      for (let v = 0; v < this.path.length; v++) {
        const S = this.path[v];
        S.shouldResetTransform = !0, (typeof S.latestValues.x == "string" || typeof S.latestValues.y == "string") && (S.isLayoutDirty = !0), S.updateScroll("snapshot"), S.options.layoutRoot && S.willUpdate(!1);
      }
      const { layoutId: y, layout: g } = this.options;
      if (y === void 0 && !g)
        return;
      const m = this.getTransformTemplate();
      this.prevTransformTemplateValue = m ? m(this.latestValues, "") : void 0, this.updateSnapshot(), h && this.notifyListeners("willUpdate");
    }
    update() {
      if (this.updateScheduled = !1, this.isUpdateBlocked()) {
        const g = this.updateBlockedByResize;
        this.unblockUpdate(), this.updateBlockedByResize = !1, this.clearAllSnapshots(), g && this.nodes.forEach(_2), this.nodes.forEach(hp);
        return;
      }
      if (this.animationId <= this.animationCommitId) {
        this.nodes.forEach(dp);
        return;
      }
      this.animationCommitId = this.animationId, this.isUpdating ? (this.isUpdating = !1, this.nodes.forEach(U2), this.nodes.forEach(B2), this.nodes.forEach(C2), this.nodes.forEach(z2)) : this.nodes.forEach(dp), this.clearAllSnapshots();
      const y = oe.now();
      ie.delta = Ie(0, 1e3 / 60, y - ie.timestamp), ie.timestamp = y, ie.isProcessing = !0, Qr.update.process(ie), Qr.preRender.process(ie), Qr.render.process(ie), ie.isProcessing = !1;
    }
    didUpdate() {
      this.updateScheduled || (this.updateScheduled = !0, $c.read(this.scheduleUpdate));
    }
    clearAllSnapshots() {
      this.nodes.forEach(V2), this.sharedNodes.forEach(L2);
    }
    scheduleUpdateProjection() {
      this.projectionUpdateScheduled || (this.projectionUpdateScheduled = !0, Ot.preRender(this.updateProjection, !1, !0));
    }
    scheduleCheckAfterUnmount() {
      Ot.postRender(() => {
        this.isLayoutDirty ? this.root.didUpdate() : this.root.checkUpdateFailed();
      });
    }
    /**
     * Update measurements
     */
    updateSnapshot() {
      this.snapshot || !this.instance || (this.snapshot = this.measure(), this.snapshot && !re(this.snapshot.measuredBox.x) && !re(this.snapshot.measuredBox.y) && (this.snapshot = void 0));
    }
    updateLayout() {
      if (!this.instance || (this.updateScroll(), !(this.options.alwaysMeasureLayout && this.isLead()) && !this.isLayoutDirty))
        return;
      if (this.resumeFrom && !this.resumeFrom.instance)
        for (let g = 0; g < this.path.length; g++)
          this.path[g].updateScroll();
      const h = this.layout;
      this.layout = this.measure(!1), this.layoutVersion++, this.layoutCorrected || (this.layoutCorrected = kt()), this.isLayoutDirty = !1, this.projectionDelta = void 0, this.notifyListeners("measure", this.layout.layoutBox);
      const { visualElement: y } = this.options;
      y && y.notify("LayoutMeasure", this.layout.layoutBox, h ? h.layoutBox : void 0);
    }
    updateScroll(h = "measure") {
      let y = !!(this.options.layoutScroll && this.instance);
      if (this.scroll && this.scroll.animationId === this.root.animationId && this.scroll.phase === h && (y = !1), y && this.instance) {
        const g = o(this.instance);
        this.scroll = {
          animationId: this.root.animationId,
          phase: h,
          isRoot: g,
          offset: u(this.instance),
          wasRoot: this.scroll ? this.scroll.isRoot : g
        };
      }
    }
    resetTransform() {
      if (!c)
        return;
      const h = this.isLayoutDirty || this.shouldResetTransform || this.options.alwaysMeasureLayout, y = this.projectionDelta && !Ig(this.projectionDelta), g = this.getTransformTemplate(), m = g ? g(this.latestValues, "") : void 0, v = m !== this.prevTransformTemplateValue;
      h && this.instance && (y || yi(this.latestValues) || v) && (c(this.instance, m), this.shouldResetTransform = !1, this.scheduleRender());
    }
    measure(h = !0) {
      const y = this.measurePageBox();
      let g = this.removeElementScroll(y);
      return h && (g = this.removeTransform(g)), G2(g), {
        animationId: this.root.animationId,
        measuredBox: y,
        layoutBox: g,
        latestValues: {},
        source: this.id
      };
    }
    measurePageBox() {
      const { visualElement: h } = this.options;
      if (!h)
        return kt();
      const y = h.measureViewportBox();
      if (!(this.scroll?.wasRoot || this.path.some(X2))) {
        const { scroll: m } = this.root;
        m && (Pe(y.x, m.offset.x), Pe(y.y, m.offset.y));
      }
      return y;
    }
    removeElementScroll(h) {
      const y = kt();
      if (Xe(y, h), this.scroll?.wasRoot)
        return y;
      for (let g = 0; g < this.path.length; g++) {
        const m = this.path[g], { scroll: v, options: S } = m;
        m !== this.root && v && S.layoutScroll && (v.wasRoot && Xe(y, h), Pe(y.x, v.offset.x), Pe(y.y, v.offset.y));
      }
      return y;
    }
    applyTransform(h, y = !1, g) {
      const m = g || kt();
      Xe(m, h);
      for (let v = 0; v < this.path.length; v++) {
        const S = this.path[v];
        !y && S.options.layoutScroll && S.scroll && S !== S.root && (Pe(m.x, -S.scroll.offset.x), Pe(m.y, -S.scroll.offset.y)), yi(S.latestValues) && tu(m, S.latestValues, S.layout?.layoutBox);
      }
      return yi(this.latestValues) && tu(m, this.latestValues, this.layout?.layoutBox), m;
    }
    removeTransform(h) {
      const y = kt();
      Xe(y, h);
      for (let g = 0; g < this.path.length; g++) {
        const m = this.path[g];
        if (!yi(m.latestValues))
          continue;
        let v;
        m.instance && (Dc(m.latestValues) && m.updateSnapshot(), v = kt(), Xe(v, m.measurePageBox())), ip(y, m.latestValues, m.snapshot?.layoutBox, v);
      }
      return yi(this.latestValues) && ip(y, this.latestValues), y;
    }
    setTargetDelta(h) {
      this.targetDelta = h, this.root.scheduleUpdateProjection(), this.isProjectionDirty = !0;
    }
    setOptions(h) {
      this.options = {
        ...this.options,
        ...h,
        crossfade: h.crossfade !== void 0 ? h.crossfade : !0
      };
    }
    clearMeasurements() {
      this.scroll = void 0, this.layout = void 0, this.snapshot = void 0, this.prevTransformTemplateValue = void 0, this.targetDelta = void 0, this.target = void 0, this.isLayoutDirty = !1;
    }
    forceRelativeParentToResolveTarget() {
      this.relativeParent && this.relativeParent.resolvedRelativeTargetAt !== ie.timestamp && this.relativeParent.resolveTargetDelta(!0);
    }
    resolveTargetDelta(h = !1) {
      const y = this.getLead();
      this.isProjectionDirty || (this.isProjectionDirty = y.isProjectionDirty), this.isTransformDirty || (this.isTransformDirty = y.isTransformDirty), this.isSharedProjectionDirty || (this.isSharedProjectionDirty = y.isSharedProjectionDirty);
      const g = !!this.resumingFrom || this !== y;
      if (!(h || g && this.isSharedProjectionDirty || this.isProjectionDirty || this.parent?.isProjectionDirty || this.attemptToResolveRelativeTarget || this.root.updateBlockedByResize))
        return;
      const { layout: v, layoutId: S } = this.options;
      if (!this.layout || !(v || S))
        return;
      this.resolvedRelativeTargetAt = ie.timestamp;
      const b = this.getClosestProjectingParent();
      b && this.linkedParentVersion !== b.layoutVersion && !b.options.layoutRoot && this.removeRelativeTarget(), !this.targetDelta && !this.relativeTarget && (this.options.layoutAnchor !== !1 && b && b.layout ? this.createRelativeTarget(b, this.layout.layoutBox, b.layout.layoutBox) : this.removeRelativeTarget()), !(!this.relativeTarget && !this.targetDelta) && (this.target || (this.target = kt(), this.targetWithTransforms = kt()), this.relativeTarget && this.relativeTargetOrigin && this.relativeParent && this.relativeParent.target ? (this.forceRelativeParentToResolveTarget(), c2(this.target, this.relativeTarget, this.relativeParent.target, this.options.layoutAnchor || void 0)) : this.targetDelta ? (this.resumingFrom ? this.applyTransform(this.layout.layoutBox, !1, this.target) : Xe(this.target, this.layout.layoutBox), qg(this.target, this.targetDelta)) : Xe(this.target, this.layout.layoutBox), this.attemptToResolveRelativeTarget && (this.attemptToResolveRelativeTarget = !1, this.options.layoutAnchor !== !1 && b && !!b.resumingFrom == !!this.resumingFrom && !b.options.layoutScroll && b.target && this.animationProgress !== 1 ? this.createRelativeTarget(b, this.target, b.target) : this.relativeParent = this.relativeTarget = void 0));
    }
    getClosestProjectingParent() {
      if (!(!this.parent || Dc(this.parent.latestValues) || Yg(this.parent.latestValues)))
        return this.parent.isProjecting() ? this.parent : this.parent.getClosestProjectingParent();
    }
    isProjecting() {
      return !!((this.relativeTarget || this.targetDelta || this.options.layoutRoot) && this.layout);
    }
    createRelativeTarget(h, y, g) {
      this.relativeParent = h, this.linkedParentVersion = h.layoutVersion, this.forceRelativeParentToResolveTarget(), this.relativeTarget = kt(), this.relativeTargetOrigin = kt(), fu(this.relativeTargetOrigin, y, g, this.options.layoutAnchor || void 0), Xe(this.relativeTarget, this.relativeTargetOrigin);
    }
    removeRelativeTarget() {
      this.relativeParent = this.relativeTarget = void 0;
    }
    calcProjection() {
      const h = this.getLead(), y = !!this.resumingFrom || this !== h;
      let g = !0;
      if ((this.isProjectionDirty || this.parent?.isProjectionDirty) && (g = !1), y && (this.isSharedProjectionDirty || this.isTransformDirty) && (g = !1), this.resolvedRelativeTargetAt === ie.timestamp && (g = !1), g)
        return;
      const { layout: m, layoutId: v } = this.options;
      if (this.isTreeAnimating = !!(this.parent && this.parent.isTreeAnimating || this.currentAnimation || this.pendingAnimation), this.isTreeAnimating || (this.targetDelta = this.relativeTarget = void 0), !this.layout || !(m || v))
        return;
      Xe(this.layoutCorrected, this.layout.layoutBox);
      const S = this.treeScale.x, b = this.treeScale.y;
      Hb(this.layoutCorrected, this.treeScale, this.path, y), h.layout && !h.target && (this.treeScale.x !== 1 || this.treeScale.y !== 1) && (h.target = h.layout.layoutBox, h.targetWithTransforms = kt());
      const { target: _ } = h;
      if (!_) {
        this.prevProjectionDelta && (this.createProjectionDeltas(), this.scheduleRender());
        return;
      }
      !this.projectionDelta || !this.prevProjectionDelta ? this.createProjectionDeltas() : (Py(this.prevProjectionDelta.x, this.projectionDelta.x), Py(this.prevProjectionDelta.y, this.projectionDelta.y)), hl(this.projectionDelta, this.layoutCorrected, _, this.latestValues), (this.treeScale.x !== S || this.treeScale.y !== b || !op(this.projectionDelta.x, this.prevProjectionDelta.x) || !op(this.projectionDelta.y, this.prevProjectionDelta.y)) && (this.hasProjected = !0, this.scheduleRender(), this.notifyListeners("projectionUpdate", _));
    }
    hide() {
      this.isVisible = !1;
    }
    show() {
      this.isVisible = !0;
    }
    scheduleRender(h = !0) {
      if (this.options.visualElement?.scheduleRender(), h) {
        const y = this.getStack();
        y && y.scheduleRender();
      }
      this.resumingFrom && !this.resumingFrom.instance && (this.resumingFrom = void 0);
    }
    createProjectionDeltas() {
      this.prevProjectionDelta = ua(), this.projectionDelta = ua(), this.projectionDeltaWithTransform = ua();
    }
    setAnimationOrigin(h, y = !1, g) {
      const m = this.snapshot, v = m ? m.latestValues : {}, S = { ...this.latestValues }, b = ua();
      (!this.relativeParent || !this.relativeParent.options.layoutRoot) && (this.relativeTarget = this.relativeTargetOrigin = void 0), this.attemptToResolveRelativeTarget = !y;
      const _ = kt(), z = m ? m.source : void 0, j = this.layout ? this.layout.source : void 0, w = z !== j, L = this.getStack(), G = !L || L.members.length <= 1, H = !!(w && !G && this.options.crossfade === !0 && !this.path.some(Y2));
      this.animationProgress = 0;
      let Y;
      const tt = g?.interpolateProjection(h);
      this.mixTargetDelta = (nt) => {
        const Q = nt / 1e3, K = tt?.(Q);
        K ? (b.x.translate = K.x, b.x.scale = Rt(h.x.scale, 1, Q), b.x.origin = h.x.origin, b.x.originPoint = h.x.originPoint, b.y.translate = K.y, b.y.scale = Rt(h.y.scale, 1, Q), b.y.origin = h.y.origin, b.y.originPoint = h.y.originPoint) : (yp(b.x, h.x, Q), yp(b.y, h.y, Q)), this.setTargetDelta(b), this.relativeTarget && this.relativeTargetOrigin && this.layout && this.relativeParent && this.relativeParent.layout && (fu(_, this.layout.layoutBox, this.relativeParent.layout.layoutBox, this.options.layoutAnchor || void 0), H2(this.relativeTarget, this.relativeTargetOrigin, _, Q), Y && m2(this.relativeTarget, Y) && (this.isProjectionDirty = !1), Y || (Y = kt()), Xe(Y, this.relativeTarget)), w && (this.animationValues = S, g2(S, v, this.latestValues, Q, H, G)), K && K.rotate !== void 0 && (this.animationValues || (this.animationValues = S), this.animationValues.pathRotation = K.rotate), this.root.scheduleUpdateProjection(), this.scheduleRender(), this.animationProgress = Q;
      }, this.mixTargetDelta(this.options.layoutRoot ? 1e3 : 0);
    }
    startAnimation(h) {
      this.notifyListeners("animationStart"), this.currentAnimation?.stop(), this.resumingFrom?.currentAnimation?.stop(), this.pendingAnimation && (Jn(this.pendingAnimation), this.pendingAnimation = void 0), this.pendingAnimation = Ot.update(() => {
        nu.hasAnimatedSinceResize = !0, this.motionValue || (this.motionValue = ra(0)), this.motionValue.jump(0, !1), this.currentAnimation = T2(this.motionValue, [0, 1e3], {
          ...h,
          velocity: 0,
          isSync: !0,
          onUpdate: (y) => {
            this.mixTargetDelta(y), h.onUpdate && h.onUpdate(y);
          },
          onComplete: () => {
            h.onComplete && h.onComplete(), this.completeAnimation();
          }
        }), this.resumingFrom && (this.resumingFrom.currentAnimation = this.currentAnimation), this.pendingAnimation = void 0;
      });
    }
    completeAnimation() {
      this.resumingFrom && (this.resumingFrom.currentAnimation = void 0, this.resumingFrom.preserveOpacity = void 0);
      const h = this.getStack();
      h && h.exitAnimationComplete(), this.resumingFrom = this.currentAnimation = this.animationValues = void 0, this.notifyListeners("animationComplete");
    }
    finishAnimation() {
      this.currentAnimation && (this.mixTargetDelta && this.mixTargetDelta(M2), this.currentAnimation.stop()), this.completeAnimation();
    }
    applyTransformsToTarget() {
      const h = this.getLead();
      let { targetWithTransforms: y, target: g, layout: m, latestValues: v } = h;
      if (!(!y || !g || !m)) {
        if (this !== h && this.layout && m && a0(this.options.animationType, this.layout.layoutBox, m.layoutBox)) {
          g = this.target || kt();
          const S = re(this.layout.layoutBox.x);
          g.x.min = h.target.x.min, g.x.max = g.x.min + S;
          const b = re(this.layout.layoutBox.y);
          g.y.min = h.target.y.min, g.y.max = g.y.min + b;
        }
        Xe(y, g), tu(y, v), hl(this.projectionDeltaWithTransform, this.layoutCorrected, y, v);
      }
    }
    registerSharedNode(h, y) {
      this.sharedNodes.has(h) || this.sharedNodes.set(h, new x2()), this.sharedNodes.get(h).add(y);
      const m = y.options.initialPromotionConfig;
      y.promote({
        transition: m ? m.transition : void 0,
        preserveFollowOpacity: m && m.shouldPreserveFollowOpacity ? m.shouldPreserveFollowOpacity(y) : void 0
      });
    }
    isLead() {
      const h = this.getStack();
      return h ? h.lead === this : !0;
    }
    getLead() {
      const { layoutId: h } = this.options;
      return h ? this.getStack()?.lead || this : this;
    }
    getPrevLead() {
      const { layoutId: h } = this.options;
      return h ? this.getStack()?.prevLead : void 0;
    }
    getStack() {
      const { layoutId: h } = this.options;
      if (h)
        return this.root.sharedNodes.get(h);
    }
    promote({ needsReset: h, transition: y, preserveFollowOpacity: g } = {}) {
      const m = this.getStack();
      m && m.promote(this, g), h && (this.projectionDelta = void 0, this.needsReset = !0), y && this.setOptions({ transition: y });
    }
    relegate() {
      const h = this.getStack();
      return h ? h.relegate(this) : !1;
    }
    resetSkewAndRotation() {
      const { visualElement: h } = this.options;
      if (!h)
        return;
      let y = !1;
      const { latestValues: g } = h;
      if ((g.z || g.rotate || g.rotateX || g.rotateY || g.rotateZ || g.skewX || g.skewY) && (y = !0), !y)
        return;
      const m = {};
      g.z && tc("z", h, m, this.animationValues);
      for (let v = 0; v < Ir.length; v++)
        tc(`rotate${Ir[v]}`, h, m, this.animationValues), tc(`skew${Ir[v]}`, h, m, this.animationValues);
      h.render();
      for (const v in m)
        h.setStaticValue(v, m[v]), this.animationValues && (this.animationValues[v] = m[v]);
      h.scheduleRender();
    }
    applyProjectionStyles(h, y) {
      if (!this.instance || this.isSVG)
        return;
      if (!this.isVisible) {
        h.visibility = "hidden";
        return;
      }
      const g = this.getTransformTemplate();
      if (this.needsReset) {
        this.needsReset = !1, h.visibility = "", h.opacity = "", h.pointerEvents = eu(y?.pointerEvents) || "", h.transform = g ? g(this.latestValues, "") : "none";
        return;
      }
      const m = this.getLead();
      if (!this.projectionDelta || !this.layout || !m.target) {
        this.options.layoutId && (h.opacity = this.latestValues.opacity !== void 0 ? this.latestValues.opacity : 1, h.pointerEvents = eu(y?.pointerEvents) || ""), this.hasProjected && !yi(this.latestValues) && (h.transform = g ? g({}, "") : "none", this.hasProjected = !1);
        return;
      }
      h.visibility = "";
      const v = m.animationValues || m.latestValues;
      this.applyTransformsToTarget();
      let S = y2(this.projectionDeltaWithTransform, this.treeScale, v);
      g && (S = g(v, S)), h.transform = S;
      const { x: b, y: _ } = this.projectionDelta;
      h.transformOrigin = `${b.origin * 100}% ${_.origin * 100}% 0`, m.animationValues ? h.opacity = m === this ? v.opacity ?? this.latestValues.opacity ?? 1 : this.preserveOpacity ? this.latestValues.opacity : v.opacityExit : h.opacity = m === this ? v.opacity !== void 0 ? v.opacity : "" : v.opacityExit !== void 0 ? v.opacityExit : 0;
      for (const z in zc) {
        if (v[z] === void 0)
          continue;
        const { correct: j, applyTo: w, isCSSVariable: L } = zc[z], G = S === "none" ? v[z] : j(v[z], m);
        if (w) {
          const H = w.length;
          for (let Y = 0; Y < H; Y++)
            h[w[Y]] = G;
        } else
          L ? this.options.visualElement.renderState.vars[z] = G : h[z] = G;
      }
      this.options.layoutId && (h.pointerEvents = m === this ? eu(y?.pointerEvents) || "" : "none");
    }
    clearSnapshot() {
      this.resumeFrom = this.snapshot = void 0;
    }
    // Only run on root
    resetTree() {
      this.root.nodes.forEach((h) => h.currentAnimation?.stop()), this.root.nodes.forEach(hp), this.root.sharedNodes.clear();
    }
  };
}
function C2(i) {
  i.updateLayout();
}
function z2(i) {
  const l = i.resumeFrom?.snapshot || i.snapshot;
  if (i.isLead() && i.layout && l && i.hasListeners("didUpdate")) {
    const { layoutBox: u, measuredBox: o } = i.layout, { animationType: c } = i.options, d = l.source !== i.layout.source;
    if (c === "size")
      We((v) => {
        const S = d ? l.measuredBox[v] : l.layoutBox[v], b = re(S);
        S.min = u[v].min, S.max = S.min + b;
      });
    else if (c === "x" || c === "y") {
      const v = c === "x" ? "y" : "x";
      Rc(d ? l.measuredBox[v] : l.layoutBox[v], u[v]);
    } else a0(c, l.layoutBox, u) && We((v) => {
      const S = d ? l.measuredBox[v] : l.layoutBox[v], b = re(u[v]);
      S.max = S.min + b, i.relativeTarget && !i.currentAnimation && (i.isProjectionDirty = !0, i.relativeTarget[v].max = i.relativeTarget[v].min + b);
    });
    const h = ua();
    hl(h, u, l.layoutBox);
    const y = ua();
    d ? hl(y, i.applyTransform(o, !0), l.measuredBox) : hl(y, u, l.layoutBox);
    const g = !Ig(h);
    let m = !1;
    if (!i.resumeFrom) {
      const v = i.getClosestProjectingParent();
      if (v && !v.resumeFrom) {
        const { snapshot: S, layout: b } = v;
        if (S && b) {
          const _ = i.options.layoutAnchor || void 0, z = kt();
          fu(z, l.layoutBox, S.layoutBox, _);
          const j = kt();
          fu(j, u, b.layoutBox, _), t0(z, j) || (m = !0), v.options.layoutRoot && (i.relativeTarget = j, i.relativeTargetOrigin = z, i.relativeParent = v);
        }
      }
    }
    i.notifyListeners("didUpdate", {
      layout: u,
      snapshot: l,
      delta: y,
      layoutDelta: h,
      hasLayoutChanged: g,
      hasRelativeLayoutChanged: m
    });
  } else if (i.isLead()) {
    const { onExitComplete: u } = i.options;
    u && u();
  }
  i.options.transition = void 0;
}
function R2(i) {
  i.parent && (i.isProjecting() || (i.isProjectionDirty = i.parent.isProjectionDirty), i.isSharedProjectionDirty || (i.isSharedProjectionDirty = !!(i.isProjectionDirty || i.parent.isProjectionDirty || i.parent.isSharedProjectionDirty)), i.isTransformDirty || (i.isTransformDirty = i.parent.isTransformDirty));
}
function O2(i) {
  i.isProjectionDirty = i.isSharedProjectionDirty = i.isTransformDirty = !1;
}
function V2(i) {
  i.clearSnapshot();
}
function hp(i) {
  i.clearMeasurements();
}
function _2(i) {
  i.isLayoutDirty = !0, i.updateLayout();
}
function dp(i) {
  i.isLayoutDirty = !1;
}
function U2(i) {
  i.isAnimationBlocked && i.layout && !i.isLayoutDirty && (i.snapshot = i.layout, i.isLayoutDirty = !0);
}
function B2(i) {
  const { visualElement: l } = i.options;
  l && l.getProps().onBeforeLayoutMeasure && l.notify("BeforeLayoutMeasure"), i.resetTransform();
}
function mp(i) {
  i.finishAnimation(), i.targetDelta = i.relativeTarget = i.target = void 0, i.isProjectionDirty = !0;
}
function N2(i) {
  i.resolveTargetDelta();
}
function j2(i) {
  i.calcProjection();
}
function w2(i) {
  i.resetSkewAndRotation();
}
function L2(i) {
  i.removeLeadSnapshot();
}
function yp(i, l, u) {
  i.translate = Rt(l.translate, 0, u), i.scale = Rt(l.scale, 1, u), i.origin = l.origin, i.originPoint = l.originPoint;
}
function pp(i, l, u, o) {
  i.min = Rt(l.min, u.min, o), i.max = Rt(l.max, u.max, o);
}
function H2(i, l, u, o) {
  pp(i.x, l.x, u.x, o), pp(i.y, l.y, u.y, o);
}
function Y2(i) {
  return i.animationValues && i.animationValues.opacityExit !== void 0;
}
const q2 = {
  duration: 0.45,
  ease: [0.4, 0, 0.1, 1]
}, gp = (i) => typeof navigator < "u" && navigator.userAgent && navigator.userAgent.toLowerCase().includes(i), vp = gp("applewebkit/") && !gp("chrome/") ? Math.round : He;
function Sp(i) {
  i.min = vp(i.min), i.max = vp(i.max);
}
function G2(i) {
  Sp(i.x), Sp(i.y);
}
function a0(i, l, u) {
  return i === "position" || i === "preserve-aspect" && !r2(up(l), up(u), 0.2);
}
function X2(i) {
  return i !== i.root && i.scroll?.wasRoot;
}
const Z2 = i0({
  attachResizeListener: (i, l) => gl(i, "resize", l),
  measureScroll: () => ({
    x: document.documentElement.scrollLeft || document.body?.scrollLeft || 0,
    y: document.documentElement.scrollTop || document.body?.scrollTop || 0
  }),
  checkIsScrollRoot: () => !0
}), ec = {
  current: void 0
}, l0 = i0({
  measureScroll: (i) => ({
    x: i.scrollLeft,
    y: i.scrollTop
  }),
  defaultParent: () => {
    if (!ec.current) {
      const i = new Z2({});
      i.mount(window), i.setOptions({ layoutScroll: !0 }), ec.current = i;
    }
    return ec.current;
  },
  resetTransform: (i, l) => {
    i.style.transform = l !== void 0 ? l : "none";
  },
  checkIsScrollRoot: (i) => window.getComputedStyle(i).position === "fixed"
}), vl = q.createContext({
  transformPagePoint: (i) => i,
  isStatic: !1,
  reducedMotion: "never"
});
function Tp(i, l) {
  if (typeof i == "function")
    return i(l);
  i != null && (i.current = l);
}
function Q2(...i) {
  return (l) => {
    let u = !1;
    const o = i.map((c) => {
      const d = Tp(c, l);
      return !u && typeof d == "function" && (u = !0), d;
    });
    if (u)
      return () => {
        for (let c = 0; c < o.length; c++) {
          const d = o[c];
          typeof d == "function" ? d() : Tp(i[c], null);
        }
      };
  };
}
function K2(...i) {
  return q.useCallback(Q2(...i), i);
}
class J2 extends q.Component {
  getSnapshotBeforeUpdate(l) {
    const u = this.props.childRef.current;
    if (Fs(u) && l.isPresent && !this.props.isPresent && this.props.pop !== !1) {
      const o = u.offsetParent, c = Fs(o) && o.offsetWidth || 0, d = Fs(o) && o.offsetHeight || 0, h = getComputedStyle(u), y = this.props.sizeRef.current;
      y.height = parseFloat(h.height), y.width = parseFloat(h.width), y.top = u.offsetTop, y.left = u.offsetLeft, y.right = c - y.width - y.left, y.bottom = d - y.height - y.top, y.direction = h.direction;
    }
    return null;
  }
  /**
   * Required with getSnapshotBeforeUpdate to stop React complaining.
   */
  componentDidUpdate() {
  }
  render() {
    return this.props.children;
  }
}
function k2({ children: i, isPresent: l, anchorX: u, anchorY: o, root: c, pop: d }) {
  const h = q.useId(), y = q.useRef(null), g = q.useRef({
    width: 0,
    height: 0,
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    direction: "ltr"
  }), { nonce: m } = q.useContext(vl), v = d !== !1 ? i.props?.ref ?? i?.ref : void 0, S = K2(y, v);
  return q.useInsertionEffect(() => {
    const { width: b, height: _, top: z, left: j, right: w, bottom: L, direction: G } = g.current;
    if (l || d === !1 || !y.current || !b || !_)
      return;
    const H = G === "rtl", Y = u === "left" ? H ? `right: ${w}` : `left: ${j}` : H ? `left: ${j}` : `right: ${w}`, tt = o === "bottom" ? `bottom: ${L}` : `top: ${z}`;
    y.current.dataset.motionPopId = h;
    const nt = document.createElement("style");
    m && (nt.nonce = m);
    const Q = c ?? document.head;
    return Q.appendChild(nt), nt.sheet && nt.sheet.insertRule(`
          [data-motion-pop-id="${h}"] {
            position: absolute !important;
            width: ${b}px !important;
            height: ${_}px !important;
            ${Y}px !important;
            ${tt}px !important;
          }
        `), () => {
      y.current?.removeAttribute("data-motion-pop-id"), Q.contains(nt) && Q.removeChild(nt);
    };
  }, [l]), rt.jsx(J2, { isPresent: l, childRef: y, sizeRef: g, pop: d, children: d === !1 ? i : q.cloneElement(i, { ref: S }) });
}
const F2 = ({ children: i, initial: l, isPresent: u, onExitComplete: o, custom: c, presenceAffectsLayout: d, mode: h, anchorX: y, anchorY: g, root: m }) => {
  const v = du(W2), S = q.useId(), b = q.useRef(u), _ = q.useRef(o);
  Bc(() => {
    b.current = u, _.current = o;
  });
  let z = !0, j = q.useMemo(() => (z = !1, {
    id: S,
    initial: l,
    isPresent: u,
    custom: c,
    onExitComplete: (w) => {
      v.set(w, !0);
      for (const L of v.values())
        if (!L)
          return;
      o && o();
    },
    register: (w) => (v.set(w, !1), () => {
      v.delete(w), !b.current && !v.size && _.current?.();
    })
  }), [u, v, o]);
  return d && z && (j = { ...j }), q.useMemo(() => {
    v.forEach((w, L) => v.set(L, !1));
  }, [u]), q.useEffect(() => {
    !u && !v.size && o && o();
  }, [u]), i = rt.jsx(k2, { pop: h === "popLayout", isPresent: u, anchorX: y, anchorY: g, root: m, children: i }), rt.jsx(mu.Provider, { value: j, children: i });
};
function W2() {
  return /* @__PURE__ */ new Map();
}
function s0(i = !0) {
  const l = q.useContext(mu);
  if (l === null)
    return [!0, null];
  const { isPresent: u, onExitComplete: o, register: c } = l, d = q.useId();
  q.useEffect(() => {
    if (i)
      return c(d);
  }, [i]);
  const h = q.useCallback(() => i && o && o(d), [d, o, i]);
  return !u && o ? [!1, h] : [!0];
}
const Zs = (i) => i.key || "";
function bp(i) {
  const l = [];
  return q.Children.forEach(i, (u) => {
    q.isValidElement(u) && l.push(u);
  }), l;
}
const P2 = ({ children: i, custom: l, initial: u = !0, onExitComplete: o, presenceAffectsLayout: c = !0, mode: d = "sync", propagate: h = !1, anchorX: y = "left", anchorY: g = "top", root: m }) => {
  const [v, S] = s0(h), b = q.useMemo(() => bp(i), [i]), _ = h && !v ? [] : b.map(Zs), z = q.useRef(!0), j = q.useRef(b), w = du(() => /* @__PURE__ */ new Map()), L = q.useRef(/* @__PURE__ */ new Set()), [G, H] = q.useState(b), [Y, tt] = q.useState(b);
  Bc(() => {
    z.current = !1, j.current = b;
    for (let K = 0; K < Y.length; K++) {
      const it = Zs(Y[K]);
      _.includes(it) ? (w.delete(it), L.current.delete(it)) : w.get(it) !== !0 && w.set(it, !1);
    }
  }, [Y, _.length, _.join("-")]);
  const nt = [];
  if (b !== G) {
    let K = [...b];
    for (let it = 0; it < Y.length; it++) {
      const $ = Y[it], yt = Zs($);
      _.includes(yt) || (K.splice(it, 0, $), nt.push($));
    }
    return d === "wait" && nt.length && (K = nt), tt(bp(K)), H(b), null;
  }
  const { forceRender: Q } = q.useContext(Uc);
  return rt.jsx(rt.Fragment, { children: Y.map((K) => {
    const it = Zs(K), $ = h && !v ? !1 : b === Y || _.includes(it), yt = () => {
      if (L.current.has(it))
        return;
      if (w.has(it))
        L.current.add(it), w.set(it, !0);
      else
        return;
      let vt = !0;
      w.forEach((Pt) => {
        Pt || (vt = !1);
      }), vt && (Q?.(), tt(j.current), h && S?.(), o && o());
    };
    return rt.jsx(F2, { isPresent: $, initial: !z.current || u ? void 0 : !1, custom: l, presenceAffectsLayout: c, mode: d, root: m, onExitComplete: $ ? void 0 : yt, anchorX: y, anchorY: g, children: K }, it);
  }) });
}, u0 = q.createContext({ strict: !1 }), Ap = {
  animation: [
    "animate",
    "variants",
    "whileHover",
    "whileTap",
    "exit",
    "whileInView",
    "whileFocus",
    "whileDrag"
  ],
  exit: ["exit"],
  drag: ["drag", "dragControls"],
  focus: ["whileFocus"],
  hover: ["whileHover", "onHoverStart", "onHoverEnd"],
  tap: ["whileTap", "onTap", "onTapStart", "onTapCancel"],
  pan: ["onPan", "onPanStart", "onPanSessionStart", "onPanEnd"],
  inView: ["whileInView", "onViewportEnter", "onViewportLeave"],
  layout: ["layout", "layoutId"]
};
let Ep = !1;
function $2() {
  if (Ep)
    return;
  const i = {};
  for (const l in Ap)
    i[l] = {
      isEnabled: (u) => Ap[l].some((o) => !!u[o])
    };
  wg(i), Ep = !0;
}
function o0() {
  return $2(), Nb();
}
function I2(i) {
  const l = o0();
  for (const u in i)
    l[u] = {
      ...l[u],
      ...i[u]
    };
  wg(l);
}
const tA = /* @__PURE__ */ new Set([
  "animate",
  "exit",
  "variants",
  "initial",
  "style",
  "values",
  "variants",
  "transition",
  "transformTemplate",
  "custom",
  "inherit",
  "onBeforeLayoutMeasure",
  "onAnimationStart",
  "onAnimationComplete",
  "onUpdate",
  "onDragStart",
  "onDrag",
  "onDragEnd",
  "onMeasureDragConstraints",
  "onDirectionLock",
  "onDragTransitionEnd",
  "_dragX",
  "_dragY",
  "onHoverStart",
  "onHoverEnd",
  "onViewportEnter",
  "onViewportLeave",
  "globalTapTarget",
  "propagate",
  "ignoreStrict",
  "viewport"
]);
function hu(i) {
  return i.startsWith("while") || i.startsWith("drag") && i !== "draggable" || i.startsWith("layout") || i.startsWith("onTap") || i.startsWith("onPan") || i.startsWith("onLayout") || tA.has(i);
}
let r0 = (i) => !hu(i);
function c0(i) {
  typeof i == "function" && (r0 = (l) => l.startsWith("on") ? !hu(l) : i(l));
}
try {
  c0(require("@emotion/is-prop-valid").default);
} catch {
}
function eA(i, l, u) {
  const o = {};
  for (const c in i)
    c === "values" && typeof i.values == "object" || ae(i[c]) || (r0(c) || u === !0 && hu(c) || !l && !hu(c) || // If trying to use native HTML drag events, forward drag listeners
    i.draggable && c.startsWith("onDrag")) && (o[c] = i[c]);
  return o;
}
function nA({ children: i, isValidProp: l, ...u }) {
  l && c0(l);
  const o = q.useContext(vl);
  u = { ...o, ...u }, u.transition = Kc(u.transition, o.transition), u.isStatic = du(() => u.isStatic);
  const c = q.useMemo(() => u, [
    JSON.stringify(u.transition),
    u.transformPagePoint,
    u.reducedMotion,
    u.skipAnimations
  ]);
  return rt.jsx(vl.Provider, { value: c, children: i });
}
const Su = /* @__PURE__ */ q.createContext({});
function iA(i, l) {
  if (vu(i)) {
    const { initial: u, animate: o } = i;
    return {
      initial: u === !1 || pl(u) ? u : void 0,
      animate: pl(o) ? o : void 0
    };
  }
  return i.inherit !== !1 ? l : {};
}
function aA(i) {
  const { initial: l, animate: u } = iA(i, q.useContext(Su));
  return q.useMemo(() => ({ initial: l, animate: u }), [xp(l), xp(u)]);
}
function xp(i) {
  return Array.isArray(i) ? i.join(" ") : i;
}
const sf = () => ({
  style: {},
  transform: {},
  transformOrigin: {},
  vars: {}
});
function f0(i, l, u) {
  for (const o in l)
    !ae(l[o]) && !Zg(o, u) && (i[o] = l[o]);
}
function lA({ transformTemplate: i }, l) {
  return q.useMemo(() => {
    const u = sf();
    return af(u, l, i), Object.assign({}, u.vars, u.style);
  }, [l]);
}
function sA(i, l) {
  const u = i.style || {}, o = {};
  return f0(o, u, i), Object.assign(o, lA(i, l)), o;
}
function uA(i, l) {
  const u = {}, o = sA(i, l);
  return i.drag && i.dragListener !== !1 && (u.draggable = !1, o.userSelect = o.WebkitUserSelect = o.WebkitTouchCallout = "none", o.touchAction = i.drag === !0 ? "none" : `pan-${i.drag === "x" ? "y" : "x"}`), i.tabIndex === void 0 && (i.onTap || i.onTapStart || i.whileTap) && (u.tabIndex = 0), u.style = o, u;
}
const h0 = () => ({
  ...sf(),
  attrs: {}
});
function oA(i, l, u, o) {
  const c = q.useMemo(() => {
    const d = h0();
    return Qg(d, l, Jg(o), i.transformTemplate, i.style), {
      ...d.attrs,
      style: { ...d.style }
    };
  }, [l]);
  if (i.style) {
    const d = {};
    f0(d, i.style, i), c.style = { ...d, ...c.style };
  }
  return c;
}
const rA = [
  "animate",
  "circle",
  "defs",
  "desc",
  "ellipse",
  "g",
  "image",
  "line",
  "filter",
  "marker",
  "mask",
  "metadata",
  "path",
  "pattern",
  "polygon",
  "polyline",
  "rect",
  "stop",
  "switch",
  "symbol",
  "svg",
  "text",
  "tspan",
  "use",
  "view"
];
function uf(i) {
  return (
    /**
     * If it's not a string, it's a custom React component. Currently we only support
     * HTML custom React components.
     */
    typeof i != "string" || /**
     * If it contains a dash, the element is a custom HTML webcomponent.
     */
    i.includes("-") ? !1 : (
      /**
       * If it's in our list of lowercase SVG tags, it's an SVG component
       */
      !!(rA.indexOf(i) > -1 || /**
       * If it contains a capital letter, it's an SVG component
       */
      /[A-Z]/u.test(i))
    )
  );
}
function cA(i, l, u, { latestValues: o }, c, d = !1, h) {
  const g = (h ?? uf(i) ? oA : uA)(l, o, c, i), m = eA(l, typeof i == "string", d), v = i !== q.Fragment ? { ...m, ...g, ref: u } : {}, { children: S } = l, b = q.useMemo(() => ae(S) ? S.get() : S, [S]);
  return q.createElement(i, {
    ...v,
    children: b
  });
}
function fA({ scrapeMotionValuesFromProps: i, createRenderState: l }, u, o, c) {
  return {
    latestValues: hA(u, o, c, i),
    renderState: l()
  };
}
function hA(i, l, u, o) {
  const c = {}, d = o(i, {});
  for (const b in d)
    c[b] = eu(d[b]);
  let { initial: h, animate: y } = i;
  const g = vu(i), m = Ng(i);
  l && m && !g && i.inherit !== !1 && (h === void 0 && (h = l.initial), y === void 0 && (y = l.animate));
  let v = u ? u.initial === !1 : !1;
  v = v || h === !1;
  const S = v ? y : h;
  if (S && typeof S != "boolean" && !gu(S)) {
    const b = Array.isArray(S) ? S : [S];
    for (let _ = 0; _ < b.length; _++) {
      const z = Fc(i, b[_]);
      if (z) {
        const { transitionEnd: j, transition: w, ...L } = z;
        for (const G in L) {
          let H = L[G];
          if (Array.isArray(H)) {
            const Y = v ? H.length - 1 : 0;
            H = H[Y];
          }
          H !== null && (c[G] = H);
        }
        for (const G in j)
          c[G] = j[G];
      }
    }
  }
  return c;
}
const d0 = (i) => (l, u) => {
  const o = q.useContext(Su), c = q.useContext(mu), d = () => fA(i, l, o, c);
  return u ? d() : du(d);
}, dA = /* @__PURE__ */ d0({
  scrapeMotionValuesFromProps: lf,
  createRenderState: sf
}), mA = /* @__PURE__ */ d0({
  scrapeMotionValuesFromProps: kg,
  createRenderState: h0
}), yA = /* @__PURE__ */ Symbol.for("motionComponentSymbol");
function pA(i, l, u) {
  const o = q.useRef(u);
  q.useInsertionEffect(() => {
    o.current = u;
  });
  const c = q.useRef(null);
  return q.useCallback((d) => {
    d && i.onMount?.(d), l && (d ? l.mount(d) : l.unmount());
    const h = o.current;
    if (typeof h == "function")
      if (d) {
        const y = h(d);
        typeof y == "function" && (c.current = y);
      } else c.current ? (c.current(), c.current = null) : h(d);
    else h && (h.current = d);
  }, [l]);
}
const m0 = q.createContext({});
function aa(i) {
  return i && typeof i == "object" && Object.prototype.hasOwnProperty.call(i, "current");
}
function gA(i, l, u, o, c, d) {
  const { visualElement: h } = q.useContext(Su), y = q.useContext(u0), g = q.useContext(mu), m = q.useContext(vl), v = m.reducedMotion, S = m.skipAnimations, b = q.useRef(null), _ = q.useRef(!1);
  o = o || y.renderer, !b.current && o && (b.current = o(i, {
    visualState: l,
    parent: h,
    props: u,
    presenceContext: g,
    blockInitialAnimation: g ? g.initial === !1 : !1,
    reducedMotionConfig: v,
    skipAnimations: S,
    isSVG: d
  }), _.current && b.current && (b.current.manuallyAnimateOnMount = !0));
  const z = b.current, j = q.useContext(m0);
  z && !z.projection && c && (z.type === "html" || z.type === "svg") && vA(b.current, u, c, j);
  const w = q.useRef(!1);
  q.useInsertionEffect(() => {
    z && w.current && z.update(u, g);
  });
  const L = u[Eg], G = q.useRef(!!L && typeof window < "u" && !window.MotionHandoffIsComplete?.(L) && window.MotionHasOptimisedAnimation?.(L));
  return Bc(() => {
    _.current = !0, z && (w.current = !0, window.MotionIsMounted = !0, z.updateFeatures(), z.scheduleRenderMicrotask(), G.current && z.animationState && z.animationState.animateChanges());
  }), q.useEffect(() => {
    z && (!G.current && z.animationState && z.animationState.animateChanges(), G.current && (queueMicrotask(() => {
      window.MotionHandoffMarkAsComplete?.(L);
    }), G.current = !1), z.enteringChildren = void 0);
  }), z;
}
function vA(i, l, u, o) {
  const { layoutId: c, layout: d, drag: h, dragConstraints: y, layoutScroll: g, layoutRoot: m, layoutAnchor: v, layoutCrossfade: S } = l;
  i.projection = new u(i.latestValues, l["data-framer-portal-id"] ? void 0 : y0(i.parent)), i.projection.setOptions({
    layoutId: c,
    layout: d,
    alwaysMeasureLayout: !!h || y && aa(y),
    visualElement: i,
    /**
     * TODO: Update options in an effect. This could be tricky as it'll be too late
     * to update by the time layout animations run.
     * We also need to fix this safeToRemove by linking it up to the one returned by usePresence,
     * ensuring it gets called if there's no potential layout animations.
     *
     */
    animationType: typeof d == "string" ? d : "both",
    initialPromotionConfig: o,
    crossfade: S,
    layoutScroll: g,
    layoutRoot: m,
    layoutAnchor: v
  });
}
function y0(i) {
  if (i)
    return i.options.allowProjection !== !1 ? i.projection : y0(i.parent);
}
function nc(i, { forwardMotionProps: l = !1, type: u } = {}, o, c) {
  o && I2(o);
  const d = u ? u === "svg" : uf(i), h = d ? mA : dA;
  function y(m, v) {
    let S;
    const b = {
      ...q.useContext(vl),
      ...m,
      layoutId: SA(m)
    }, { isStatic: _ } = b, z = aA(m), j = h(m, _);
    if (!_ && typeof window < "u") {
      TA();
      const w = bA(b);
      S = w.MeasureLayout, z.visualElement = gA(i, j, b, c, w.ProjectionNode, d);
    }
    return rt.jsxs(Su.Provider, { value: z, children: [S && z.visualElement ? rt.jsx(S, { visualElement: z.visualElement, ...b }) : null, cA(i, m, pA(j, z.visualElement, v), j, _, l, d)] });
  }
  y.displayName = `motion.${typeof i == "string" ? i : `create(${i.displayName ?? i.name ?? ""})`}`;
  const g = q.forwardRef(y);
  return g[yA] = i, g;
}
function SA({ layoutId: i }) {
  const l = q.useContext(Uc).id;
  return l && i !== void 0 ? l + "-" + i : i;
}
function TA(i, l) {
  q.useContext(u0).strict;
}
function bA(i) {
  const l = o0(), { drag: u, layout: o } = l;
  if (!u && !o)
    return {};
  const c = { ...u, ...o };
  return {
    MeasureLayout: u?.isEnabled(i) || o?.isEnabled(i) ? c.MeasureLayout : void 0,
    ProjectionNode: c.ProjectionNode
  };
}
function AA(i, l) {
  if (typeof Proxy > "u")
    return nc;
  const u = /* @__PURE__ */ new Map(), o = (d, h) => nc(d, h, i, l), c = (d, h) => o(d, h);
  return new Proxy(c, {
    /**
     * Called when `motion` is referenced with a prop: `motion.div`, `motion.input` etc.
     * The prop name is passed through as `key` and we can use that to generate a `motion`
     * DOM component with that name.
     */
    get: (d, h) => h === "create" ? o : (u.has(h) || u.set(h, nc(h, void 0, i, l)), u.get(h))
  });
}
const EA = (i, l) => l.isSVG ?? uf(i) ? new $b(l) : new Kb(l, {
  allowProjection: i !== q.Fragment
});
class xA extends kn {
  /**
   * We dynamically generate the AnimationState manager as it contains a reference
   * to the underlying animation library. We only want to load that if we load this,
   * so people can optionally code split it out using the `m` component.
   */
  constructor(l) {
    super(l), l.animationState || (l.animationState = i2(l));
  }
  updateAnimationControlsSubscription() {
    const { animate: l } = this.node.getProps();
    gu(l) && (this.unmountControls = l.subscribe(this.node));
  }
  /**
   * Subscribe any provided AnimationControls to the component's VisualElement
   */
  mount() {
    this.updateAnimationControlsSubscription();
  }
  update() {
    const { animate: l } = this.node.getProps(), { animate: u } = this.node.prevProps || {};
    l !== u && this.updateAnimationControlsSubscription();
  }
  unmount() {
    this.node.animationState.reset(), this.unmountControls?.();
  }
}
let MA = 0;
class DA extends kn {
  constructor() {
    super(...arguments), this.id = MA++, this.isExitComplete = !1;
  }
  update() {
    if (!this.node.presenceContext)
      return;
    const { isPresent: l, onExitComplete: u } = this.node.presenceContext, { isPresent: o } = this.node.prevPresenceContext || {};
    if (!this.node.animationState || l === o)
      return;
    if (l && o === !1) {
      if (this.isExitComplete) {
        const { initial: d, custom: h } = this.node.getProps();
        if (typeof d == "string" || typeof d == "object" && d !== null && !Array.isArray(d)) {
          const y = Si(this.node, d, h);
          if (y) {
            const { transition: g, transitionEnd: m, ...v } = y;
            for (const S in v)
              this.node.getValue(S)?.jump(v[S]);
          }
        }
        this.node.animationState.reset(), this.node.animationState.animateChanges();
      } else
        this.node.animationState.setActive("exit", !1);
      this.isExitComplete = !1;
      return;
    }
    const c = this.node.animationState.setActive("exit", !l);
    u && !l && c.then(() => {
      this.isExitComplete = !0, u(this.id);
    });
  }
  mount() {
    const { register: l, onExitComplete: u } = this.node.presenceContext || {};
    u && u(this.id), l && (this.unmount = l(this.id));
  }
  unmount() {
  }
}
const CA = {
  animation: {
    Feature: xA
  },
  exit: {
    Feature: DA
  }
};
function El(i) {
  return {
    point: {
      x: i.pageX,
      y: i.pageY
    }
  };
}
const zA = (i) => (l) => Ic(l) && i(l, El(l));
function dl(i, l, u, o) {
  return gl(i, l, zA(u), o);
}
const p0 = ({ current: i }) => i ? i.ownerDocument.defaultView : null, Mp = (i, l) => Math.abs(i - l);
function RA(i, l) {
  const u = Mp(i.x, l.x), o = Mp(i.y, l.y);
  return Math.sqrt(u ** 2 + o ** 2);
}
const Dp = /* @__PURE__ */ new Set(["auto", "scroll"]);
class g0 {
  constructor(l, u, { transformPagePoint: o, contextWindow: c = window, dragSnapToOrigin: d = !1, distanceThreshold: h = 3, element: y } = {}) {
    if (this.startEvent = null, this.lastMoveEvent = null, this.lastMoveEventInfo = null, this.lastRawMoveEventInfo = null, this.handlers = {}, this.contextWindow = window, this.scrollPositions = /* @__PURE__ */ new Map(), this.removeScrollListeners = null, this.onElementScroll = (z) => {
      this.handleScroll(z.target);
    }, this.onWindowScroll = () => {
      this.handleScroll(window);
    }, this.updatePoint = () => {
      if (!(this.lastMoveEvent && this.lastMoveEventInfo))
        return;
      this.lastRawMoveEventInfo && (this.lastMoveEventInfo = Qs(this.lastRawMoveEventInfo, this.transformPagePoint));
      const z = ic(this.lastMoveEventInfo, this.history), j = this.startEvent !== null, w = RA(z.offset, { x: 0, y: 0 }) >= this.distanceThreshold;
      if (!j && !w)
        return;
      const { point: L } = z, { timestamp: G } = ie;
      this.history.push({ ...L, timestamp: G });
      const { onStart: H, onMove: Y } = this.handlers;
      j || (H && H(this.lastMoveEvent, z), this.startEvent = this.lastMoveEvent), Y && Y(this.lastMoveEvent, z);
    }, this.handlePointerMove = (z, j) => {
      this.lastMoveEvent = z, this.lastRawMoveEventInfo = j, this.lastMoveEventInfo = Qs(j, this.transformPagePoint), Ot.update(this.updatePoint, !0);
    }, this.handlePointerUp = (z, j) => {
      this.end();
      const { onEnd: w, onSessionEnd: L, resumeAnimation: G } = this.handlers;
      if ((this.dragSnapToOrigin || !this.startEvent) && G && G(), !(this.lastMoveEvent && this.lastMoveEventInfo))
        return;
      const H = ic(z.type === "pointercancel" ? this.lastMoveEventInfo : Qs(j, this.transformPagePoint), this.history);
      this.startEvent && w && w(z, H), L && L(z, H);
    }, !Ic(l))
      return;
    this.dragSnapToOrigin = d, this.handlers = u, this.transformPagePoint = o, this.distanceThreshold = h, this.contextWindow = c || window;
    const g = El(l), m = Qs(g, this.transformPagePoint), { point: v } = m, { timestamp: S } = ie;
    this.history = [{ ...v, timestamp: S }];
    const { onSessionStart: b } = u;
    b && b(l, ic(m, this.history));
    const _ = { passive: !0, capture: !0 };
    this.removeListeners = Tl(dl(this.contextWindow, "pointermove", this.handlePointerMove, _), dl(this.contextWindow, "pointerup", this.handlePointerUp, _), dl(this.contextWindow, "pointercancel", this.handlePointerUp, _)), y && this.startScrollTracking(y);
  }
  /**
   * Start tracking scroll on ancestors and window.
   */
  startScrollTracking(l) {
    let u = l.parentElement;
    for (; u; ) {
      const o = getComputedStyle(u);
      (Dp.has(o.overflowX) || Dp.has(o.overflowY)) && this.scrollPositions.set(u, {
        x: u.scrollLeft,
        y: u.scrollTop
      }), u = u.parentElement;
    }
    this.scrollPositions.set(window, {
      x: window.scrollX,
      y: window.scrollY
    }), window.addEventListener("scroll", this.onElementScroll, {
      capture: !0
    }), window.addEventListener("scroll", this.onWindowScroll), this.removeScrollListeners = () => {
      window.removeEventListener("scroll", this.onElementScroll, {
        capture: !0
      }), window.removeEventListener("scroll", this.onWindowScroll);
    };
  }
  /**
   * Handle scroll compensation during drag.
   *
   * For element scroll: adjusts history origin since pageX/pageY doesn't change.
   * For window scroll: adjusts lastMoveEventInfo since pageX/pageY would change.
   */
  handleScroll(l) {
    const u = this.scrollPositions.get(l);
    if (!u)
      return;
    const o = l === window, c = o ? { x: window.scrollX, y: window.scrollY } : {
      x: l.scrollLeft,
      y: l.scrollTop
    }, d = { x: c.x - u.x, y: c.y - u.y };
    d.x === 0 && d.y === 0 || (o ? this.lastMoveEventInfo && (this.lastMoveEventInfo.point.x += d.x, this.lastMoveEventInfo.point.y += d.y) : this.history.length > 0 && (this.history[0].x -= d.x, this.history[0].y -= d.y), this.scrollPositions.set(l, c), Ot.update(this.updatePoint, !0));
  }
  updateHandlers(l) {
    this.handlers = l;
  }
  end() {
    this.removeListeners && this.removeListeners(), this.removeScrollListeners && this.removeScrollListeners(), this.scrollPositions.clear(), Jn(this.updatePoint);
  }
}
function Qs(i, l) {
  return l ? { point: l(i.point) } : i;
}
function Cp(i, l) {
  return { x: i.x - l.x, y: i.y - l.y };
}
function ic({ point: i }, l) {
  return {
    point: i,
    delta: Cp(i, v0(l)),
    offset: Cp(i, OA(l)),
    velocity: VA(l, 0.1)
  };
}
function OA(i) {
  return i[0];
}
function v0(i) {
  return i[i.length - 1];
}
function VA(i, l) {
  if (i.length < 2)
    return { x: 0, y: 0 };
  let u = i.length - 1, o = null;
  const c = v0(i);
  for (; u >= 0 && (o = i[u], !(c.timestamp - o.timestamp > /* @__PURE__ */ Ce(l))); )
    u--;
  if (!o)
    return { x: 0, y: 0 };
  o === i[0] && i.length > 2 && c.timestamp - o.timestamp > /* @__PURE__ */ Ce(l) * 2 && (o = i[1]);
  const d = /* @__PURE__ */ Le(c.timestamp - o.timestamp);
  if (d === 0)
    return { x: 0, y: 0 };
  const h = {
    x: (c.x - o.x) / d,
    y: (c.y - o.y) / d
  };
  return h.x === 1 / 0 && (h.x = 0), h.y === 1 / 0 && (h.y = 0), h;
}
function _A(i, { min: l, max: u }, o) {
  return l !== void 0 && i < l ? i = o ? Rt(l, i, o.min) : Math.max(i, l) : u !== void 0 && i > u && (i = o ? Rt(u, i, o.max) : Math.min(i, u)), i;
}
function zp(i, l, u) {
  return {
    min: l !== void 0 ? i.min + l : void 0,
    max: u !== void 0 ? i.max + u - (i.max - i.min) : void 0
  };
}
function UA(i, { top: l, left: u, bottom: o, right: c }) {
  return {
    x: zp(i.x, u, c),
    y: zp(i.y, l, o)
  };
}
function Rp(i, l) {
  let u = l.min - i.min, o = l.max - i.max;
  return l.max - l.min < i.max - i.min && ([u, o] = [o, u]), { min: u, max: o };
}
function BA(i, l) {
  return {
    x: Rp(i.x, l.x),
    y: Rp(i.y, l.y)
  };
}
function NA(i, l) {
  let u = 0.5;
  const o = re(i), c = re(l);
  return c > o ? u = /* @__PURE__ */ ml(l.min, l.max - o, i.min) : o > c && (u = /* @__PURE__ */ ml(i.min, i.max - c, l.min)), Ie(0, 1, u);
}
function jA(i, l) {
  const u = {};
  return l.min !== void 0 && (u.min = l.min - i.min), l.max !== void 0 && (u.max = l.max - i.min), u;
}
const Oc = 0.35;
function wA(i = Oc) {
  return i === !1 ? i = 0 : i === !0 && (i = Oc), {
    x: Op(i, "left", "right"),
    y: Op(i, "top", "bottom")
  };
}
function Op(i, l, u) {
  return {
    min: Vp(i, l),
    max: Vp(i, u)
  };
}
function Vp(i, l) {
  return typeof i == "number" ? i : i[l] || 0;
}
const LA = /* @__PURE__ */ new WeakMap();
class HA {
  constructor(l) {
    this.openDragLock = null, this.isDragging = !1, this.currentDirection = null, this.originPoint = { x: 0, y: 0 }, this.constraints = !1, this.hasMutatedConstraints = !1, this.elastic = kt(), this.latestPointerEvent = null, this.latestPanInfo = null, this.visualElement = l;
  }
  start(l, { snapToCursor: u = !1, distanceThreshold: o } = {}) {
    const { presenceContext: c } = this.visualElement;
    if (c && c.isPresent === !1)
      return;
    const d = (S) => {
      u && this.snapToCursor(El(S).point), this.stopAnimation();
    }, h = (S, b) => {
      const { drag: _, dragPropagation: z, onDragStart: j } = this.getProps();
      if (_ && !z && (this.openDragLock && this.openDragLock(), this.openDragLock = fb(_), !this.openDragLock))
        return;
      this.latestPointerEvent = S, this.latestPanInfo = b, this.isDragging = !0, this.currentDirection = null, this.resolveConstraints(), this.visualElement.projection && (this.visualElement.projection.isAnimationBlocked = !0, this.visualElement.projection.target = void 0), We((L) => {
        let G = this.getAxisMotionValue(L).get() || 0;
        if ($e.test(G)) {
          const { projection: H } = this.visualElement;
          if (H && H.layout) {
            const Y = H.layout.layoutBox[L];
            Y && (G = re(Y) * (parseFloat(G) / 100));
          }
        }
        this.originPoint[L] = G;
      }), j && Ot.update(() => j(S, b), !1, !0), Tc(this.visualElement, "transform");
      const { animationState: w } = this.visualElement;
      w && w.setActive("whileDrag", !0);
    }, y = (S, b) => {
      this.latestPointerEvent = S, this.latestPanInfo = b;
      const { dragPropagation: _, dragDirectionLock: z, onDirectionLock: j, onDrag: w } = this.getProps();
      if (!_ && !this.openDragLock)
        return;
      const { offset: L } = b;
      if (z && this.currentDirection === null) {
        this.currentDirection = qA(L), this.currentDirection !== null && j && j(this.currentDirection);
        return;
      }
      this.updateAxis("x", b.point, L), this.updateAxis("y", b.point, L), this.visualElement.render(), w && Ot.update(() => w(S, b), !1, !0);
    }, g = (S, b) => {
      this.latestPointerEvent = S, this.latestPanInfo = b, this.stop(S, b), this.latestPointerEvent = null, this.latestPanInfo = null;
    }, m = () => {
      const { dragSnapToOrigin: S } = this.getProps();
      (S || this.constraints) && this.startAnimation({ x: 0, y: 0 });
    }, { dragSnapToOrigin: v } = this.getProps();
    this.panSession = new g0(l, {
      onSessionStart: d,
      onStart: h,
      onMove: y,
      onSessionEnd: g,
      resumeAnimation: m
    }, {
      transformPagePoint: this.visualElement.getTransformPagePoint(),
      dragSnapToOrigin: v,
      distanceThreshold: o,
      contextWindow: p0(this.visualElement),
      element: this.visualElement.current
    });
  }
  /**
   * @internal
   */
  stop(l, u) {
    const o = l || this.latestPointerEvent, c = u || this.latestPanInfo, d = this.isDragging;
    if (this.cancel(), !d || !c || !o)
      return;
    const { velocity: h } = c;
    this.startAnimation(h);
    const { onDragEnd: y } = this.getProps();
    y && Ot.postRender(() => y(o, c));
  }
  /**
   * @internal
   */
  cancel() {
    this.isDragging = !1;
    const { projection: l, animationState: u } = this.visualElement;
    l && (l.isAnimationBlocked = !1), this.endPanSession();
    const { dragPropagation: o } = this.getProps();
    !o && this.openDragLock && (this.openDragLock(), this.openDragLock = null), u && u.setActive("whileDrag", !1);
  }
  /**
   * Clean up the pan session without modifying other drag state.
   * This is used during unmount to ensure event listeners are removed
   * without affecting projection animations or drag locks.
   * @internal
   */
  endPanSession() {
    this.panSession && this.panSession.end(), this.panSession = void 0;
  }
  updateAxis(l, u, o) {
    const { drag: c } = this.getProps();
    if (!o || !Ks(l, c, this.currentDirection))
      return;
    const d = this.getAxisMotionValue(l);
    let h = this.originPoint[l] + o[l];
    this.constraints && this.constraints[l] && (h = _A(h, this.constraints[l], this.elastic[l])), d.set(h);
  }
  resolveConstraints() {
    const { dragConstraints: l, dragElastic: u } = this.getProps(), o = this.visualElement.projection && !this.visualElement.projection.layout ? this.visualElement.projection.measure(!1) : this.visualElement.projection?.layout, c = this.constraints;
    l && aa(l) ? this.constraints || (this.constraints = this.resolveRefConstraints()) : l && o ? this.constraints = UA(o.layoutBox, l) : this.constraints = !1, this.elastic = wA(u), c !== this.constraints && !aa(l) && o && this.constraints && !this.hasMutatedConstraints && We((d) => {
      this.constraints !== !1 && this.getAxisMotionValue(d) && (this.constraints[d] = jA(o.layoutBox[d], this.constraints[d]));
    });
  }
  resolveRefConstraints() {
    const { dragConstraints: l, onMeasureDragConstraints: u } = this.getProps();
    if (!l || !aa(l))
      return !1;
    const o = l.current, { projection: c } = this.visualElement;
    if (!c || !c.layout)
      return !1;
    c.root && (c.root.scroll = void 0, c.root.updateScroll());
    const d = Yb(o, c.root, this.visualElement.getTransformPagePoint());
    let h = BA(c.layout.layoutBox, d);
    if (u) {
      const y = u(wb(h));
      this.hasMutatedConstraints = !!y, y && (h = Hg(y));
    }
    return h;
  }
  startAnimation(l) {
    const { drag: u, dragMomentum: o, dragElastic: c, dragTransition: d, dragSnapToOrigin: h, onDragTransitionEnd: y } = this.getProps(), g = this.constraints || {}, m = We((v) => {
      if (!Ks(v, u, this.currentDirection))
        return;
      let S = g && g[v] || {};
      (h === !0 || h === v) && (S = { min: 0, max: 0 });
      const b = c ? 200 : 1e6, _ = c ? 40 : 1e7, z = {
        type: "inertia",
        velocity: o ? l[v] : 0,
        bounceStiffness: b,
        bounceDamping: _,
        timeConstant: 750,
        restDelta: 1,
        restSpeed: 10,
        ...d,
        ...S
      };
      return this.startAxisValueAnimation(v, z);
    });
    return Promise.all(m).then(y);
  }
  startAxisValueAnimation(l, u) {
    const o = this.getAxisMotionValue(l);
    return Tc(this.visualElement, l), o.start(kc(l, o, 0, u, this.visualElement, !1));
  }
  stopAnimation() {
    We((l) => this.getAxisMotionValue(l).stop());
  }
  /**
   * Drag works differently depending on which props are provided.
   *
   * - If _dragX and _dragY are provided, we output the gesture delta directly to those motion values.
   * - Otherwise, we apply the delta to the x/y motion values.
   */
  getAxisMotionValue(l) {
    const u = `_drag${l.toUpperCase()}`, c = this.visualElement.getProps()[u];
    return c || this.visualElement.getValue(l, this.visualElement.latestValues[l] ?? 0);
  }
  snapToCursor(l) {
    We((u) => {
      const { drag: o } = this.getProps();
      if (!Ks(u, o, this.currentDirection))
        return;
      const { projection: c } = this.visualElement, d = this.getAxisMotionValue(u);
      if (c && c.layout) {
        const { min: h, max: y } = c.layout.layoutBox[u], g = d.get() || 0;
        d.set(l[u] - Rt(h, y, 0.5) + g);
      }
    });
  }
  /**
   * When the viewport resizes we want to check if the measured constraints
   * have changed and, if so, reposition the element within those new constraints
   * relative to where it was before the resize.
   */
  scalePositionWithinConstraints() {
    if (!this.visualElement.current)
      return;
    const { drag: l, dragConstraints: u } = this.getProps(), { projection: o } = this.visualElement;
    if (!aa(u) || !o || !this.constraints)
      return;
    this.stopAnimation();
    const c = { x: 0, y: 0 };
    We((h) => {
      const y = this.getAxisMotionValue(h);
      if (y && this.constraints !== !1) {
        const g = y.get();
        c[h] = NA({ min: g, max: g }, this.constraints[h]);
      }
    });
    const { transformTemplate: d } = this.visualElement.getProps();
    this.visualElement.current.style.transform = d ? d({}, "") : "none", o.root && o.root.updateScroll(), o.updateLayout(), this.constraints = !1, this.resolveConstraints(), We((h) => {
      if (!Ks(h, l, null))
        return;
      const y = this.getAxisMotionValue(h), { min: g, max: m } = this.constraints[h];
      y.set(Rt(g, m, c[h]));
    }), this.visualElement.render();
  }
  addListeners() {
    if (!this.visualElement.current)
      return;
    LA.set(this.visualElement, this);
    const l = this.visualElement.current, u = dl(l, "pointerdown", (m) => {
      const { drag: v, dragListener: S = !0 } = this.getProps(), b = m.target, _ = b !== l && gb(b);
      v && S && !_ && this.start(m);
    });
    let o;
    const c = () => {
      const { dragConstraints: m } = this.getProps();
      aa(m) && m.current && (this.constraints = this.resolveRefConstraints(), o || (o = YA(l, m.current, () => this.scalePositionWithinConstraints())));
    }, { projection: d } = this.visualElement, h = d.addEventListener("measure", c);
    d && !d.layout && (d.root && d.root.updateScroll(), d.updateLayout()), Ot.read(c);
    const y = gl(window, "resize", () => this.scalePositionWithinConstraints()), g = d.addEventListener("didUpdate", (({ delta: m, hasLayoutChanged: v }) => {
      this.isDragging && v && (We((S) => {
        const b = this.getAxisMotionValue(S);
        b && (this.originPoint[S] += m[S].translate, b.set(b.get() + m[S].translate));
      }), this.visualElement.render());
    }));
    return () => {
      y(), u(), h(), g && g(), o && o();
    };
  }
  getProps() {
    const l = this.visualElement.getProps(), { drag: u = !1, dragDirectionLock: o = !1, dragPropagation: c = !1, dragConstraints: d = !1, dragElastic: h = Oc, dragMomentum: y = !0 } = l;
    return {
      ...l,
      drag: u,
      dragDirectionLock: o,
      dragPropagation: c,
      dragConstraints: d,
      dragElastic: h,
      dragMomentum: y
    };
  }
}
function _p(i) {
  let l = !0;
  return () => {
    if (l) {
      l = !1;
      return;
    }
    i();
  };
}
function YA(i, l, u) {
  const o = Hy(i, _p(u)), c = Hy(l, _p(u));
  return () => {
    o(), c();
  };
}
function Ks(i, l, u) {
  return (l === !0 || l === i) && (u === null || u === i);
}
function qA(i, l = 10) {
  let u = null;
  return Math.abs(i.y) > l ? u = "y" : Math.abs(i.x) > l && (u = "x"), u;
}
class GA extends kn {
  constructor(l) {
    super(l), this.removeGroupControls = He, this.removeListeners = He, this.controls = new HA(l);
  }
  mount() {
    const { dragControls: l } = this.node.getProps();
    l && (this.removeGroupControls = l.subscribe(this.controls)), this.removeListeners = this.controls.addListeners() || He;
  }
  update() {
    const { dragControls: l } = this.node.getProps(), { dragControls: u } = this.node.prevProps || {};
    l !== u && (this.removeGroupControls(), l && (this.removeGroupControls = l.subscribe(this.controls)));
  }
  unmount() {
    this.removeGroupControls(), this.removeListeners(), this.controls.isDragging || this.controls.endPanSession();
  }
}
const ac = (i) => (l, u) => {
  i && Ot.update(() => i(l, u), !1, !0);
};
class XA extends kn {
  constructor() {
    super(...arguments), this.removePointerDownListener = He;
  }
  onPointerDown(l) {
    this.session = new g0(l, this.createPanHandlers(), {
      transformPagePoint: this.node.getTransformPagePoint(),
      contextWindow: p0(this.node)
    });
  }
  createPanHandlers() {
    const { onPanSessionStart: l, onPanStart: u, onPan: o, onPanEnd: c } = this.node.getProps();
    return {
      onSessionStart: ac(l),
      onStart: ac(u),
      onMove: ac(o),
      onEnd: (d, h) => {
        delete this.session, c && Ot.postRender(() => c(d, h));
      }
    };
  }
  mount() {
    this.removePointerDownListener = dl(this.node.current, "pointerdown", (l) => this.onPointerDown(l));
  }
  update() {
    this.session && this.session.updateHandlers(this.createPanHandlers());
  }
  unmount() {
    this.removePointerDownListener(), this.session && this.session.end();
  }
}
let lc = !1;
class ZA extends q.Component {
  /**
   * This only mounts projection nodes for components that
   * need measuring, we might want to do it for all components
   * in order to incorporate transforms
   */
  componentDidMount() {
    const { visualElement: l, layoutGroup: u, switchLayoutGroup: o, layoutId: c } = this.props, { projection: d } = l;
    d && (u.group && u.group.add(d), o && o.register && c && o.register(d), lc && d.root.didUpdate(), d.addEventListener("animationComplete", () => {
      this.safeToRemove();
    }), d.setOptions({
      ...d.options,
      layoutDependency: this.props.layoutDependency,
      onExitComplete: () => this.safeToRemove()
    })), nu.hasEverUpdated = !0;
  }
  getSnapshotBeforeUpdate(l) {
    const { layoutDependency: u, visualElement: o, drag: c, isPresent: d } = this.props, { projection: h } = o;
    return h && (h.isPresent = d, l.layoutDependency !== u && h.setOptions({
      ...h.options,
      layoutDependency: u
    }), lc = !0, c || l.layoutDependency !== u || u === void 0 || l.isPresent !== d ? h.willUpdate() : this.safeToRemove(), l.isPresent !== d && (d ? h.promote() : h.relegate() || Ot.postRender(() => {
      const y = h.getStack();
      (!y || !y.members.length) && this.safeToRemove();
    }))), null;
  }
  componentDidUpdate() {
    const { visualElement: l, layoutAnchor: u } = this.props, { projection: o } = l;
    o && (o.options.layoutAnchor = u, o.root.didUpdate(), $c.postRender(() => {
      !o.currentAnimation && o.isLead() && this.safeToRemove();
    }));
  }
  componentWillUnmount() {
    const { visualElement: l, layoutGroup: u, switchLayoutGroup: o } = this.props, { projection: c } = l;
    lc = !0, c && (c.scheduleCheckAfterUnmount(), u && u.group && u.group.remove(c), o && o.deregister && o.deregister(c));
  }
  safeToRemove() {
    const { safeToRemove: l } = this.props;
    l && l();
  }
  render() {
    return null;
  }
}
function S0(i) {
  const [l, u] = s0(), o = q.useContext(Uc);
  return rt.jsx(ZA, { ...i, layoutGroup: o, switchLayoutGroup: q.useContext(m0), isPresent: l, safeToRemove: u });
}
const QA = {
  pan: {
    Feature: XA
  },
  drag: {
    Feature: GA,
    ProjectionNode: l0,
    MeasureLayout: S0
  }
};
function Up(i, l, u) {
  const { props: o } = i;
  i.animationState && o.whileHover && i.animationState.setActive("whileHover", u === "Start");
  const c = "onHover" + u, d = o[c];
  d && Ot.postRender(() => d(l, El(l)));
}
class KA extends kn {
  mount() {
    const { current: l } = this.node;
    l && (this.unmount = db(l, (u, o) => (Up(this.node, o, "Start"), (c) => Up(this.node, c, "End"))));
  }
  unmount() {
  }
}
class JA extends kn {
  constructor() {
    super(...arguments), this.isActive = !1;
  }
  onFocus() {
    let l = !1;
    try {
      l = this.node.current.matches(":focus-visible");
    } catch {
      l = !0;
    }
    !l || !this.node.animationState || (this.node.animationState.setActive("whileFocus", !0), this.isActive = !0);
  }
  onBlur() {
    !this.isActive || !this.node.animationState || (this.node.animationState.setActive("whileFocus", !1), this.isActive = !1);
  }
  mount() {
    this.unmount = Tl(gl(this.node.current, "focus", () => this.onFocus()), gl(this.node.current, "blur", () => this.onBlur()));
  }
  unmount() {
  }
}
function Bp(i, l, u) {
  const { props: o } = i;
  if (i.current instanceof HTMLButtonElement && i.current.disabled)
    return;
  i.animationState && o.whileTap && i.animationState.setActive("whileTap", u === "Start");
  const c = "onTap" + (u === "End" ? "" : u), d = o[c];
  d && Ot.postRender(() => d(l, El(l)));
}
class kA extends kn {
  mount() {
    const { current: l } = this.node;
    if (!l)
      return;
    const { globalTapTarget: u, propagate: o } = this.node.props;
    this.unmount = Sb(l, (c, d) => (Bp(this.node, d, "Start"), (h, { success: y }) => Bp(this.node, h, y ? "End" : "Cancel")), {
      useGlobalTarget: u,
      stopPropagation: o?.tap === !1
    });
  }
  unmount() {
  }
}
const Vc = /* @__PURE__ */ new WeakMap(), sc = /* @__PURE__ */ new WeakMap(), FA = (i) => {
  const l = Vc.get(i.target);
  l && l(i);
}, WA = (i) => {
  i.forEach(FA);
};
function PA({ root: i, ...l }) {
  const u = i || document;
  sc.has(u) || sc.set(u, {});
  const o = sc.get(u), c = JSON.stringify(l);
  return o[c] || (o[c] = new IntersectionObserver(WA, { root: i, ...l })), o[c];
}
function $A(i, l, u) {
  const o = PA(l);
  return Vc.set(i, u), o.observe(i), () => {
    Vc.delete(i), o.unobserve(i);
  };
}
const IA = {
  some: 0,
  all: 1
};
class tE extends kn {
  constructor() {
    super(...arguments), this.hasEnteredView = !1, this.isInView = !1;
  }
  startObserver() {
    this.stopObserver?.();
    const { viewport: l = {} } = this.node.getProps(), { root: u, margin: o, amount: c = "some", once: d } = l, h = {
      root: u ? u.current : void 0,
      rootMargin: o,
      threshold: typeof c == "number" ? c : IA[c]
    }, y = (g) => {
      const { isIntersecting: m } = g;
      if (this.isInView === m || (this.isInView = m, d && !m && this.hasEnteredView))
        return;
      m && (this.hasEnteredView = !0), this.node.animationState && this.node.animationState.setActive("whileInView", m);
      const { onViewportEnter: v, onViewportLeave: S } = this.node.getProps(), b = m ? v : S;
      b && b(g);
    };
    this.stopObserver = $A(this.node.current, h, y);
  }
  mount() {
    this.startObserver();
  }
  update() {
    if (typeof IntersectionObserver > "u")
      return;
    const { props: l, prevProps: u } = this.node;
    ["amount", "margin", "root"].some(eE(l, u)) && this.startObserver();
  }
  unmount() {
    this.stopObserver?.(), this.hasEnteredView = !1, this.isInView = !1;
  }
}
function eE({ viewport: i = {} }, { viewport: l = {} } = {}) {
  return (u) => i[u] !== l[u];
}
const nE = {
  inView: {
    Feature: tE
  },
  tap: {
    Feature: kA
  },
  focus: {
    Feature: JA
  },
  hover: {
    Feature: KA
  }
}, iE = {
  layout: {
    ProjectionNode: l0,
    MeasureLayout: S0
  }
}, aE = {
  ...CA,
  ...nE,
  ...QA,
  ...iE
}, lE = /* @__PURE__ */ AA(aE, EA), Np = lE, sE = { deal: aS, liquidity: lS, treasury: nS, review: sS, result: iS };
function uE({ data: i, setStateValue: l, setTriggerValue: u }) {
  const [o, c] = q.useState(i.activeStage);
  q.useEffect(() => c(i.activeStage), [i.activeStage]);
  const d = (g) => {
    c(g), l("active_stage", g);
  }, h = (g) => {
    g.state !== "blocked" && d(g.id);
  }, y = () => {
    d("result"), u("primary_action", "run_review");
  };
  return /* @__PURE__ */ rt.jsx(nA, { reducedMotion: "user", transition: { duration: 0.2 }, children: /* @__PURE__ */ rt.jsxs("section", { className: "experience", "aria-label": i.product.title, children: [
    /* @__PURE__ */ rt.jsx("nav", { className: "stages", "aria-label": "사전점검 단계", children: i.stages.map((g) => {
      const m = sE[g.id], v = o === g.id;
      return /* @__PURE__ */ rt.jsxs("button", { className: `stage stage--${v ? "active" : g.state}`, type: "button", disabled: g.state === "blocked", "aria-current": v ? "step" : void 0, onClick: () => h(g), children: [
        /* @__PURE__ */ rt.jsx(m, { size: 19, "aria-hidden": !0 }),
        /* @__PURE__ */ rt.jsx("span", { children: g.label }),
        v && /* @__PURE__ */ rt.jsx(Np.span, { className: "stage-indicator", layoutId: "stage-indicator" })
      ] }, g.id);
    }) }),
    /* @__PURE__ */ rt.jsx(P2, { mode: "wait", children: o === "result" && /* @__PURE__ */ rt.jsxs(Np.div, { className: "stage-panel stage-panel--result", initial: { opacity: 0, y: 6 }, animate: { opacity: 1, y: 0 }, exit: { opacity: 0 }, children: [
      /* @__PURE__ */ rt.jsx("h2", { children: "현재 계산 기준 종합 결과" }),
      /* @__PURE__ */ rt.jsx("div", { className: "decision-snapshot", children: i.snapshot.map((g) => /* @__PURE__ */ rt.jsxs("div", { children: [
        /* @__PURE__ */ rt.jsx("span", { children: g.label }),
        /* @__PURE__ */ rt.jsx("strong", { children: g.value }),
        /* @__PURE__ */ rt.jsx("small", { children: g.detail })
      ] }, g.label)) }),
      /* @__PURE__ */ rt.jsx("h3", { children: "거래 검토 요약" }),
      i.reviewState.loading ? /* @__PURE__ */ rt.jsx("p", { children: "현재 거래 근거를 확인하고 있습니다." }) : i.reviewState.error ? /* @__PURE__ */ rt.jsx("p", { className: "error", children: i.reviewState.error }) : i.reviewState.current ? /* @__PURE__ */ rt.jsxs(rt.Fragment, { children: [
        /* @__PURE__ */ rt.jsx("h3", { children: i.reviewState.headline }),
        /* @__PURE__ */ rt.jsx("p", { children: i.reviewState.summary }),
        /* @__PURE__ */ rt.jsxs("details", { children: [
          /* @__PURE__ */ rt.jsx("summary", { children: "상세 설명 보기" }),
          /* @__PURE__ */ rt.jsxs("small", { children: [
            "확인 완료 · ",
            i.reviewState.usedTools?.join(" · ")
          ] })
        ] })
      ] }) : i.reviewState.hasResult ? /* @__PURE__ */ rt.jsx("p", { children: "조건이 변경되어 다시 검토가 필요합니다." }) : /* @__PURE__ */ rt.jsx("p", { className: "support", children: "현재 계산의 의미를 짧게 검토할 수 있습니다." }),
      /* @__PURE__ */ rt.jsx("button", { className: "primary-action", type: "button", disabled: !i.reviewState.ready, onClick: y, children: "이 조건으로 거래 검토" })
    ] }, o) })
  ] }) });
}
const Js = /* @__PURE__ */ new WeakMap(), rE = (i) => {
  const l = i.parentElement.querySelector(".react-root");
  if (!l)
    throw new Error("React root element not found");
  let u = Js.get(i.parentElement);
  return u || (u = $1.createRoot(l), Js.set(i.parentElement, u)), u.render(
    /* @__PURE__ */ rt.jsx(q.StrictMode, { children: /* @__PURE__ */ rt.jsx(
      uE,
      {
        data: i.data,
        setStateValue: i.setStateValue,
        setTriggerValue: i.setTriggerValue
      }
    ) })
  ), () => {
    Js.get(i.parentElement)?.unmount(), Js.delete(i.parentElement);
  };
};
export {
  rE as default
};
