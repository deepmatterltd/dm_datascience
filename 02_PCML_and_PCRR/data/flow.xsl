<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xs="http://www.w3.org/2001/XMLSchema"
  exclude-result-prefixes="xs"
  version="2.0">
  
  <xsl:output method="html" />
  <xsl:template match="pcml">
    <div class=" flowchart"  text-align="center">
      <div class="card-block">
      <h2><xsl:value-of select="@experiment"/></h2>
      <div class="container">
        <div class="flow-content">
          <div class="flow start">Start</div>
          <svg width="60" height="55" preserveAspectRatio="none">
            <path d="M20 40 L 30 50 L 40 40" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
            <path d="M30 0 L30 50" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
          </svg>
          <xsl:apply-templates />
         <div class="flow start">Stop</div>
        </div>
      </div>
      </div>
    </div>
  </xsl:template>
  <xsl:template match="operation">
    <xsl:apply-templates select="interrogation[@type='yesno'][@position='pre']/content"/>
    <xsl:apply-templates select="text"/>
    <xsl:apply-templates select="interrogation[@type='yesno'][@position='post']/content"/>
    <xsl:apply-templates select="interrogation[@type='yesno']/content"/>
  </xsl:template>

  <xsl:template match="operation/interrogation[@type='yesno']/content">
    <div class="flow interrogation">
      <div class="interrogation_content"><xsl:value-of select="."/></div>
    </div>
    <div>Yes</div>
    <svg width="60" height="55" preserveAspectRatio="none">
      <path d="M20 40 L 30 50 L 40 40" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
      <path d="M30 0 L30 50" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
    </svg>
  </xsl:template>

  <xsl:template match="operation/text">
    <div class="flow operation">
      <xsl:value-of select="."/>
    </div>
    <svg width="60" height="55"  preserveAspectRatio="none">
      <path d="M20 40 L 30 50 L 40 40" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
      <path d="M30 0 L30 50" fill="none" stroke="black" stroke-linecap="round" stroke-width="2" />
    </svg>
  </xsl:template>
  
  <xsl:template match="text()|@*">
  </xsl:template>
  
</xsl:stylesheet>