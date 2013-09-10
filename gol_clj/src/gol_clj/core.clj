(ns gol-clj.core
  (:require [gol-clj.cells :as cells])
  (:require [gol-clj.game :as game])
  (:gen-class))


(def cell-repr {:alive \# :dead \space})


(defn clear-str
  [state]
  (let [n (cells/num-rows state)
        cursor-up "\u001B[1A"
        erase-line "\u001B[2K"]
    (->> [erase-line cursor-up]
         (repeat n)
         (mapcat identity)
         (cons cursor-up)
         (apply str))))


(defn render
  "Return the world state as string to be written to stdout"
  [state]
  ((comp (partial apply str)
         (partial interpose \newline))
   (map (comp #(apply str %)
              #(map cell-repr %))
        state)))


(defn printer
  [state]
  (println (str (clear-str state) (render state))))


(def C5 [[:dead :dead :dead :dead :dead :dead]
         [:dead :dead :alive :alive :alive :dead]
         [:dead :alive :alive :alive :dead :dead]
         [:dead :dead :dead :dead :dead :dead]])


(defn -main
  "I don't do a whole lot ... yet."
  [& args]
  ;; work around dangerous default behaviour in Clojure
  (alter-var-root #'*read-eval* (constantly false))
  (let [grid (cells/grid (first args))]
    (game/start (:cells grid) printer 200)))
