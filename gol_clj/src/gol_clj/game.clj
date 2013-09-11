(ns gol-clj.game
  (:require [gol-clj.cells :as cells]))


(defn world
  "Lives on forever"
  [state fun printer ms]
  (printer state)
  (Thread/sleep ms)
  (world (fun state) fun printer ms))


(defn destiny
  "Produces next state of a cell"
  [pos status cells]
  (let [n (cells/count-neighbours pos cells)]
    (if (= status :alive)
      (if (or (= n 2) (= n 3)) :alive :dead)
      (if (= n 3) :alive :dead))))


(defn evolve
  "Evolution of the cells together"
  [state]
  (let [idx-state (cells/indexed-cells state)]
    (mapv (fn [v]
            (mapv (fn [[pos status]]
                    (destiny pos status state))
                  v))
          idx-state)))


(defn start
  "Big Bang!"
  [init printer ms]
  (world init evolve printer ms))

