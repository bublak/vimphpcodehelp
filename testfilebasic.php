<?php
# SOME php code for testing :)

namespace bublak\phpunitmultirunner\Tree;

class Mputree {
    const ABC = 'abc';
    const EDF = 'abc';

    public static $DEFAULT_COUNT = 20;

    private $_nodes = array();

    protected static $OPENSOCIAL_VIEWERID = "opensocial_viewer_id";

    private $_isRoot   = false;
    private $_fullPath = null;
    private $_filename = null;

    protected static $_consumerCommunities      = null;

    private static $_instance = null;

    private $_execTimeRating = null;
    private $_execTime       = null;

    abstract protected function setDocumentAttribute(DOMElement $document);
    protected abstract function getConfigData();
    public abstract function renderHeader(array $preparedHeader);
    abstract public function renderHeaderb(array $preparedHeader);

    protected static function sortFunction($first, $second, $rules) {
    }

    public static function getEvaluationBasePath() {
        return $ble;
    }

    protected function createDOMDocument() {
        return $ble;
    }

    private $_isRoot   = false;
    public function __construct($fullPath, $isRoot=false) {
        $this->_fullPath = $fullPath;
        $this->_isRoot = $isRoot;
    }

    public function setFullPath($path) {
        $this->_fullPath = $path;
    }

    public function setFilename($name) {
        $this->_filename = $name;
    }

    public function setNodes(array $nodes) {
        $this->_nodes[$this->fullPath] = $nodes;
    }

    public function setExecTimeRating($rating) {
        $this->_execTimeRating = $rating;
    }

    public function setExecTime($time) {
        $this->_execTime = $time;
    }

    public function addNode(Mputree $node) {
        $this->_nodes[] = $node;
    }

    public function getExecTimeRating() {
        return $this->_execTimeRating;
    }

    public function getExecTime() {
        return $this->_execTime;
    }

    public function getNodes() {
        return $this->_nodes;
    }

    public function getFullPath() {
        return $this->_fullPath;
    }

    public function getFilename() {
        return $this->_filename;
    }

    public function save($file) {
        if ($this->_isRoot === TRUE) {
            $res = serialize($this);

            $fileHandler = fopen($file, 'w');
            fwrite($fileHandler, $res);
            fclose($fileHandler);
        } else {
            return false;
        }

        return true;
    }
}

